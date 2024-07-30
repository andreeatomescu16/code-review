import sys
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def generate_feedback(diff, code_content):
    """Generate feedback using OpenAI GPT model."""
    system_message = f"""\
I will provide for you the differences extracted with a github function between
the initial and the final code and also the initial code. Please review these 
differences in the context of the initial code and identify any syntax or logical
errors, suggest ways to refactor and improve code quality, enhance performance, 
address security concerns, and align with best practices. Provide specific examples 
for each area and limit your recommendations to three per category.

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

Code changes:

{diff}

Full code:

{code_content}

Your review:"""

    response = completion(
        model="ollama/llama3",
        messages=[
            {"role": "system", "content": system_message},
        ],
        api_base="http://localhost:11434"
    )

    return response['choices'][0]['message']['content']

def review_code_diffs(diffs, file_contents):
    review_results = []
    for file_name, diff in diffs.items():
        print("The differences are:\n", diff)
        if diff:
            code_content = file_contents.get(file_name, "")
            answer = generate_feedback(diff, code_content)
            review_results.append(f"FILE: {file_name}\nDIFF: {diff}\nENDDIFF\nREVIEW: \n{answer}\nENDREVIEW")

    return "\n".join(review_results)

def get_file_diffs(file_list):
    diffs = {}
    for file_name in file_list.split():
        diff_file = f"diffs/{file_name}.diff"
        if os.path.exists(diff_file):
            with open(diff_file, 'r') as file:
                diff = file.read()
            diffs[file_name] = diff
    return diffs

def get_file_contents(file_list):
    contents = {}
    for file_name in file_list.split():
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.read()
            contents[file_name] = content
    return contents

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)

    files = sys.argv[1]
    file_diffs = get_file_diffs(files)
    file_contents = get_file_contents(files)
    result = review_code_diffs(file_diffs, file_contents)
    with open('reviews.txt', 'w') as output_file:
        output_file.write(result)
 
