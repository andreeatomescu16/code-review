import os
import subprocess
from github import Github
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Get environment variables
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
REPO_NAME = "andreeatomescu16/mygitactions"

if not GITHUB_TOKEN or not REPO_NAME:
    raise ValueError("Missing GITHUB_TOKEN or GITHUB_REPOSITORY environment variable")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def get_latest_commit_branch():
    latest_commit_date = None
    latest_commit_branch = None
    
    branches = repo.get_branches()
    for branch in branches:
        commits = repo.get_commits(sha=branch.name)
        if commits:
            latest_commit = commits[0]
            if latest_commit_date is None or latest_commit.commit.author.date > latest_commit_date:
                latest_commit_date = latest_commit.commit.author.date
                latest_commit_branch = branch.name

    return latest_commit_branch

def create_and_merge_pull_request():
    base = repo.default_branch
    head = get_latest_commit_branch()

    if head is None:
        raise ValueError("No branch found for the latest commit.")

    print(f"Latest commit branch: {head}")
    print(f"Base branch: {base}")

    if head == base:
        print(f"No new changes to merge. Both head and base are {base}.")
        return

    # Check for existing pull requests
    pulls = repo.get_pulls(state='open', head=f"{repo.owner.login}:{head}", base=base)
    if pulls.totalCount > 0:
        print(f"A pull request already exists for {head} into {base}.")
        pr = pulls[0]
    else:
        # Create a pull request
        pr_title = f"Automated PR from {head} to {base}"
        pr_body = "This pull request is automatically created."
        pr = repo.create_pull(title=pr_title, body=pr_body, head=head, base=base)
        print(f"Pull request created: {pr.html_url}")

    # Attempt to merge the pull request
    try:
        merge_result = pr.merge()
        if merge_result.merged:
            print(f"Pull request merged: {pr.html_url}")
        else:
            print(f"Failed to merge pull request: {pr.html_url}")
    except Exception as e:
        print(f"An error occurred while merging the pull request: {e}")

if __name__ == "__main__":
    create_and_merge_pull_request()
