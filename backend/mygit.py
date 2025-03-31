import os

def init_repository(repo_path):
    """
    Initializes a new repository in the given path.
    """
    mygit_path = os.path.join(repo_path, ".mygit")
    commits_path = os.path.join(mygit_path, "commits")
    branches_path = os.path.join(mygit_path, "branches")

    # Create .mygit directory
    os.makedirs(mygit_path, exist_ok=True)
    # Create commits directory
    os.makedirs(commits_path, exist_ok=True)
    # Create branches directory
    os.makedirs(branches_path, exist_ok=True)

    print(f"Repository initialized at {repo_path}")

def add_file(repo_path, file_path):
    """
    Adds a file to the repository.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # For now, we'll just print a message.
    # Later, we'll add the file to the repository's tracking system.
    print(f"Added file '{file_path}' to the repository.")

# Example usage
repo_path = "my_repo"  # The directory where you want to create the repository.
os.makedirs(repo_path, exist_ok=True) #creates the folder if it does not exist.
init_repository(repo_path)
add_file(repo_path, "example.txt") #example of how to add a file. example.txt must exist in the folder.