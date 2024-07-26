import os
import sys
from litellm import completion
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class CompletionError(Exception):
    """Custom exception for completion errors"""
    pass

@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry=retry_if_exception_type(Exception), before_sleep=before_sleep_log(logger, logging.WARNING))
def generate_feedback(diff):
    """Generate feedback using OpenAI GPT model."""
    system_message = f"""\
I will provide for you the differences extracted with a github function between the initial and the final code. 
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

Code changes:

{diff}

Your review:"""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry=retry_if_exception_type(Exception), before_sleep=before_sleep_log(logger, logging.WARNING))
    def get_completion():
        response = completion(
            model="ollama/llama3",
            messages=[
                {"role": "system", "content": system_message},
            ],
            api_base="http://localhost:11434"
        )
        return response

    try:
        response = get_completion()
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise CompletionError(f"Failed to generate feedback after 3 retries: {str(e)}")

def review_code_diffs(diffs):
    review_results = []
    for file_name, diff in diffs.items():
        print("The differences are:\n", diff)
        answer = generate_feedback(diff)
        review_results.append(f"FILE: {file_name}\nDIFF: {diff}\nENDDIFF\nREVIEW: {answer}\nENDREVIEW")
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)

    files = sys.argv[1]
    file_diffs = get_file_diffs(files)
    result = review_code_diffs(file_diffs)
    with open('reviews.txt', 'w') as output_file:
        output_file.write(result)
