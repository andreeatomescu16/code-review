import sys
import openai
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def generate_feedback(code):
    """Generate feedback using OpenAI GPT model."""
    system_message = f"""\
        Please review the code below and identify any syntax or logical errors, suggest
        ways to refactor and improve code quality, enhance performance, address security
        concerns, and align with best practices. Provide specific examples for each area
        and limit your recommendations to three per category.

        Use the following response format, keeping the section headings as-is, and provide
        your feedback. Use bullet points for each response. The provided examples are for
        illustration purposes only and should not be repeated.

        **Syntax and logical errors (example)**:
        - Incorrect indentation on line 12
        - Missing closing parenthesis on line 23

        **Code refactoring and quality (example)**:
        - Replace multiple if-else statements with a switch case for readability
        - Extract repetitive code into separate functions

        **Performance optimization (example)**:
        - Use a more efficient sorting algorithm to reduce time complexity
        - Cache results of expensive operations for reuse

        **Security vulnerabilities (example)**:
        - Sanitize user input to prevent SQL injection attacks
        - Use prepared statements for database queries

        **Best practices (example)**:
        - Add meaningful comments and documentation to explain the code
        - Follow consistent naming conventions for variables and functions

        Code:
        ```
        {code}
        ```

        Your review:"""


    response = completion(
    model="ollama/llama3",
    # model="gpt-4", 
    messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Please review the following code and provide feedback:\n\n{code}"}
        ],
    api_base="http://localhost:11434"
    )

    return response['choices'][0]['message']['content']


def review_code(files):
    review_results = []
    for file_name in files.split():
        with open(file_name, 'r') as file:
            code = file.read()

        # Perform code review and return the result
        answer = generate_feedback(code)
        review_results.append(f"Code review for {file_name}: \n{answer}\n")
    return "\n".join(review_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)

    files = sys.argv[1]
    result = review_code(files)
    print(result)
 
