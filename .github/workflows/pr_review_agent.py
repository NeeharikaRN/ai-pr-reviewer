import os
from github import Github, Auth

# Set up GitHub authentication
token = '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'  # Personal Access Token for GitHub API access
g = Github(auth=Auth.Token(token))

# GitHub repository and PR details
repo_name = "preethamkondapaka/ai-pr-reviewer"
pr_number = 1  # Replace with dynamic PR number from event

# Function to check CI/CD status
def check_pr_status(repo_name, pr_number):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Get commits from PR
    commits = pr.get_commits()  # This returns a list of commits
    
    # Loop through each commit and fetch its status
    for commit in commits:
        statuses = commit.get_statuses()  # Use get_statuses() to retrieve status checks for each commit
        
        # Check the status of the latest commit's status checks
        for status in statuses:
            if status.state == "success":
                return "approved"
            elif status.state == "error":
                return "blocked"
    
    return "waiting"

# Function to approve or block PR
def review_pr(repo_name, pr_number, decision):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    if decision == "approved":
        pr.create_review(body="PR approved by AI Agent", event="APPROVE")
    elif decision == "blocked":
        pr.create_review(body="PR blocked due to failing checks", event="REQUEST_CHANGES")
    else:
        pr.create_review(body="PR is still under review", event="COMMENT")

# Initialize LangChain agent (you can expand this for more decision-making logic)
def agent_review(pr_status):
    if pr_status == "approved":
        return "approved"
    elif pr_status == "blocked":
        return "blocked"
    else:
        return "waiting"

# Main function to trigger agent review process
def trigger_agent_review():
    pr_status = check_pr_status(repo_name, pr_number)
    decision = agent_review(pr_status)
    review_pr(repo_name, pr_number, decision)

if __name__ == "__main__":
    trigger_agent_review()
