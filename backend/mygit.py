import os
import difflib
import hashlib
import time
import json
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
def calculate_file_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# def create_commit(repo_path, message):
#     """Creates a new commit."""
#     mygit_path = os.path.join(repo_path, ".mygit")
#     commits_path = os.path.join(mygit_path, "commits")
#     current_files = {}

#     # Track current file states
#     for filename in os.listdir(repo_path):
#         filepath = os.path.join(repo_path, filename)
#         if os.path.isfile(filepath) and filename != ".mygit":
#             current_files[filename] = calculate_file_hash(filepath)

#     # Generate diffs and create commit
#     commit_id = str(int(time.time()))
#     commit_dir = os.path.join(commits_path, commit_id)
#     os.makedirs(commit_dir)

#     metadata = {
#         "message": message,
#         "timestamp": time.time(),
#         "files": {}
#     }

#     for filename, file_hash in current_files.items():
#         filepath = os.path.join(repo_path, filename)
#         metadata["files"][filename] = file_hash

#         # Store file content in commit
#         with open(filepath, 'r') as f:
#             file_content = f.read()
#         with open(os.path.join(commit_dir, filename), 'w') as f:
#             f.write(file_content)

#     # Save metadata
#     import json
#     with open(os.path.join(commit_dir, "metadata.json"), 'w') as f:
#         json.dump(metadata, f, indent=4)

#     print(f"Commit {commit_id} created: {message}")

def create_commit(repo_path, message):
    """Creates a new commit."""
    mygit_path = os.path.join(repo_path, ".mygit")
    commits_path = os.path.join(mygit_path, "commits")
    current_files = {}

    # Track current file states
    for filename in os.listdir(repo_path):
        filepath = os.path.join(repo_path, filename)
        if os.path.isfile(filepath) and filename != ".mygit":
            current_files[filename] = calculate_file_hash(filepath)

    # Generate diffs and create commit
    commit_id = str(int(time.time() * 1000))  # Use milliseconds for more precision
    commit_dir = os.path.join(commits_path, commit_id)
    os.makedirs(commit_dir)

    metadata = {
        "message": message,
        "timestamp": time.time(),
        "files": {}
    }

    for filename, file_hash in current_files.items():
        filepath = os.path.join(repo_path, filename)
        metadata["files"][filename] = file_hash

        # Store file content in commit
        with open(filepath, 'r') as f:
            file_content = f.read()
        with open(os.path.join(commit_dir, filename), 'w') as f:
            f.write(file_content)

    # Save metadata
    with open(os.path.join(commit_dir, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"Commit {commit_id} created: {message}")

# Example usage
repo_path = "my_repo"
os.makedirs(repo_path, exist_ok=True)
init_repository(repo_path)

with open(os.path.join(repo_path, "example.txt"), 'w') as f:
    f.write("Initial content\n")

create_commit(repo_path, "Initial commit")

with open(os.path.join(repo_path, "example.txt"), 'a') as f:
    f.write("Added a line\n")

create_commit(repo_path, "Added a line to example.txt")
