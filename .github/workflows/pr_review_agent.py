import os
from github import Github, Auth

# Set up GitHub authentication using the Personal Access Token (PAT)
# You can replace the token with a GitHub secret (e.g., CIagent) in your CI/CD pipeline
token = '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'  # Replace this with your GitHub Token
g = Github(auth=Auth.Token(token))  # Authenticate with the GitHub API using the token

# GitHub repository and PR details
repo_name = "preethamkondapaka/ai-pr-reviewer"  # Name of the GitHub repository
pr_number = 1  # This is the pull request number to be reviewed; replace dynamically in CI/CD

# Function to check the CI/CD status of a PR
def check_pr_status(repo_name, pr_number):
    # Get the repository and pull request objects from GitHub
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Get commits from the pull request
    commits = pr.get_commits()  # This returns a list of commits for this PR
    
    # Loop through each commit to check the CI/CD status checks (e.g., passing tests, etc.)
    for commit in commits:
        statuses = commit.get_statuses()  # Retrieves the status checks associated with the commit
        
        # Loop through each status check for the commit
        for status in statuses:
            # If the status check is successful, mark the PR as "approved"
            if status.state == "success":
                print(f"Commit {commit.sha} is successful. PR is approved.")  # Add this line for clarity
                return "approved"
            # If the status check has failed (e.g., failing tests), mark the PR as "blocked"
            elif status.state == "error":
                print(f"Commit {commit.sha} failed. PR is blocked.")  # Add this line for clarity
                return "blocked"
    
    # If no status checks are found or they are still pending, return "waiting"
    print(f"Commit statuses are still pending for PR #{pr_number}. PR is under review.")  # Add this line for clarity
    return "waiting"

# Function to approve or block the PR based on the decision
def review_pr(repo_name, pr_number, decision):
    # Get the repository and pull request objects again
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Based on the decision, create a review for the PR
    if decision == "approved":
        print(f"Approving PR #{pr_number}...")  # Add this line for clarity
        pr.create_review(body="PR approved by AI Agent", event="APPROVE")
    elif decision == "blocked":
        print(f"Blocking PR #{pr_number} due to failing checks...")  # Add this line for clarity
        pr.create_review(body="PR blocked due to failing checks", event="REQUEST_CHANGES")
    else:
        print(f"PR #{pr_number} is still under review.")  # Add this line for clarity
        pr.create_review(body="PR is still under review", event="COMMENT")

# Function that represents the AI agent's decision-making logic
# It makes a decision based on the PR status (approved, blocked, or waiting)
def agent_review(pr_status):
    print(f"AI Agent received the PR status: {pr_status}")  # Add this line for clarity

    # If PR is approved, the agent will approve the PR
    if pr_status == "approved":
        return "approved"
    # If PR is blocked (e.g., failing tests), the agent will block the PR
    elif pr_status == "blocked":
        return "blocked"
    # If PR is still waiting (e.g., CI checks are still pending), the agent will leave a comment
    else:
        return "waiting"

# Main function to trigger the entire agent review process
def trigger_agent_review():
    print("Starting the PR review process...")  # Add this line for clarity

    # Step 1: Check the current CI/CD status of the PR
    pr_status = check_pr_status(repo_name, pr_number)

    # Step 2: Let the AI agent make a decision based on the PR status
    decision = agent_review(pr_status)

    # Step 3: Review the PR based on the agent's decision (approve, block, or leave under review)
    review_pr(repo_name, pr_number, decision)

# Run the agent review process when the script is executed
if __name__ == "__main__":
    trigger_agent_review()
