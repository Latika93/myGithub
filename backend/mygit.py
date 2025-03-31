import os
import difflib
import hashlib
import time
import json
import shutil
from flask import Flask, render_template, request, redirect, url_for, jsonify


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

    # Create initial empty commit for main branch
    initial_commit_id = str(int(time.time() * 1000))
    initial_commit_dir = os.path.join(commits_path, initial_commit_id)
    os.makedirs(initial_commit_dir)

    initial_metadata = {
        "message": "Initial commit",
        "timestamp": time.time(),
        "files": {}
    }

    with open(os.path.join(initial_commit_dir, "metadata.json"), 'w') as f:
        json.dump(initial_metadata, f, indent=4)

    # Initialize main branch to point to the initial commit
    with open(os.path.join(branches_path, "main"), 'w') as f:
        f.write(initial_commit_id)

    # Initialize HEAD to main branch
    with open(os.path.join(branches_path, "HEAD"), 'w') as f:
        f.write("main")

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

def view_history(repo_path):
    """Displays the commit history."""
    commits_path = os.path.join(repo_path, ".mygit", "commits")
    commits = sorted(os.listdir(commits_path), reverse=True)

    print("Commit History:")
    for commit_id in commits:
        metadata_path = os.path.join(commits_path, commit_id, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            print(f"  Commit: {commit_id}")
            print(f"    Message: {metadata['message']}")
            print(f"    Timestamp: {time.ctime(metadata['timestamp'])}")

def revert_to_commit(repo_path, commit_id):
    """Reverts the repository to a specific commit."""
    commits_path = os.path.join(repo_path, ".mygit", "commits")
    commit_dir = os.path.join(commits_path, commit_id)
    metadata_path = os.path.join(commit_dir, "metadata.json")

    if not os.path.exists(metadata_path):
        print(f"Error: Commit {commit_id} not found.")
        return

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    for filename, file_hash in metadata["files"].items():
        commit_file_path = os.path.join(commit_dir, filename)
        repo_file_path = os.path.join(repo_path, filename)

        if os.path.exists(commit_file_path):
            with open(commit_file_path, 'r') as commit_file, open(repo_file_path, 'w') as repo_file:
                repo_file.write(commit_file.read())
            print(f"Reverted {filename} to commit {commit_id}")
        else:
            print(f"File {filename} not found in commit {commit_id}")

    print(f"Repository reverted to commit {commit_id}")

def get_status(repo_path):
    """Displays the current status of the repository."""
    current_files = {}
    for filename in os.listdir(repo_path):
        filepath = os.path.join(repo_path, filename)
        if os.path.isfile(filepath) and filename != ".mygit":
            current_files[filename] = calculate_file_hash(filepath)

    commits_path = os.path.join(repo_path, ".mygit", "commits")
    latest_commit_id = sorted(os.listdir(commits_path))[-1] #gets latest commit.
    latest_commit_metadata_path = os.path.join(commits_path, latest_commit_id, "metadata.json")

    with open(latest_commit_metadata_path, 'r') as f:
        latest_commit_metadata = json.load(f)

    modified_files = []
    for filename, file_hash in current_files.items():
        if filename not in latest_commit_metadata["files"] or latest_commit_metadata["files"][filename] != file_hash:
            modified_files.append(filename)

    print("Repository Status:")
    if modified_files:
        print("  Modified files:")
        for filename in modified_files:
            print(f"    {filename}")
    else:
        print("  No modified files.")

def create_branch(repo_path, branch_name):
    """Creates a new branch."""
    branches_path = os.path.join(repo_path, ".mygit", "branches")
    branch_file = os.path.join(branches_path, branch_name)

    if os.path.exists(branch_file):
        print(f"Error: Branch '{branch_name}' already exists.")
        return

    commits_path = os.path.join(repo_path, ".mygit", "commits")
    latest_commit_id = sorted(os.listdir(commits_path))[-1] #gets latest commit.

    with open(branch_file, 'w') as f:
        f.write(latest_commit_id)

    print(f"Branch '{branch_name}' created.")

def switch_branch(repo_path, branch_name):
    """Switches to the specified branch."""
    branches_path = os.path.join(repo_path, ".mygit", "branches")
    branch_file = os.path.join(branches_path, branch_name)

    if not os.path.exists(branch_file):
        print(f"Error: Branch '{branch_name}' does not exist.")
        return

    with open(branch_file, 'r') as f:
        commit_id = f.read().strip()

    revert_to_commit(repo_path, commit_id)

    # Update current branch pointer (for simplicity, we'll store it in a file)
    with open(os.path.join(branches_path, "HEAD"), 'w') as f:
        f.write(branch_name)

    print(f"Switched to branch '{branch_name}'.")


def merge_branches(repo_path, branch1, branch2):
    """Merges branch2 into branch1."""
    branches_path = os.path.join(repo_path, ".mygit", "branches")
    branch1_file = os.path.join(branches_path, branch1)
    branch2_file = os.path.join(branches_path, branch2)

    if not os.path.exists(branch1_file) or not os.path.exists(branch2_file):
        print("Error: One or both branches do not exist.")
        return

    with open(branch1_file, 'r') as f:
        branch1_commit_id = f.read().strip()
    with open(branch2_file, 'r') as f:
        branch2_commit_id = f.read().strip()

    branch1_commit_dir = os.path.join(repo_path, ".mygit", "commits", branch1_commit_id)
    branch2_commit_dir = os.path.join(repo_path, ".mygit", "commits", branch2_commit_id)

    # Get file contents from both branches
    branch1_files = {}
    branch2_files = {}

    with open(os.path.join(branch1_commit_dir, "metadata.json"), 'r') as f:
        branch1_metadata = json.load(f)
    with open(os.path.join(branch2_commit_dir, "metadata.json"), 'r') as f:
        branch2_metadata = json.load(f)

    for filename in branch1_metadata["files"]:
        with open(os.path.join(branch1_commit_dir, filename), 'r') as f:
            branch1_files[filename] = f.read()

    for filename in branch2_metadata["files"]:
        with open(os.path.join(branch2_commit_dir, filename), 'r') as f:
            branch2_files[filename] = f.read()

    # Merge files and handle conflicts
    merged_files = {}
    conflicts = []

    all_files = set(branch1_files.keys()) | set(branch2_files.keys())

    for filename in all_files:
        if filename in branch1_files and filename in branch2_files:
            if branch1_files[filename] == branch2_files[filename]:
                merged_files[filename] = branch1_files[filename]
            else:
                conflicts.append(filename)
                merged_files[filename] = f"<<<<<<< {branch1}\n{branch1_files[filename]}\n=======\n{branch2_files[filename]}\n>>>>>>> {branch2}"
        elif filename in branch1_files:
            merged_files[filename] = branch1_files[filename]
        else:
            merged_files[filename] = branch2_files[filename]

    # Create merge commit
    merge_commit_message = f"Merged {branch2} into {branch1}"
    merge_commit_id = str(int(time.time() * 1000))
    merge_commit_dir = os.path.join(repo_path, ".mygit", "commits", merge_commit_id)
    os.makedirs(merge_commit_dir)

    merge_metadata = {
        "message": merge_commit_message,
        "timestamp": time.time(),
        "files": {}
    }

    for filename, content in merged_files.items():
        filepath = os.path.join(merge_commit_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        merge_metadata["files"][filename] = calculate_file_hash(filepath)

    with open(os.path.join(merge_commit_dir, "metadata.json"), 'w') as f:
        json.dump(merge_metadata, f, indent=4)

    # Update branch1 to point to the merge commit
    with open(branch1_file, 'w') as f:
        f.write(merge_commit_id)

    print(f"Merged {branch2} into {branch1}.")
    if conflicts:
        print("Conflicts detected in the following files:")
        for filename in conflicts:
            print(f"  {filename}")

app = Flask(__name__)

REPO_PATH = "my_repo"  # Define the repository path
PULL_REQUESTS = []  # List to store pull requests

@app.route('/')
def index():
    """Displays the repository browser."""
    files = [f for f in os.listdir(REPO_PATH) if os.path.isfile(os.path.join(REPO_PATH, f)) and not f.startswith('.')]
    commits_path = os.path.join(REPO_PATH, ".mygit", "commits")
    commits = sorted(os.listdir(commits_path), reverse=True)
    return render_template('index.html', files=files, commits=commits, pull_requests=PULL_REQUESTS)

@app.route('/file/<filename>')
def view_file(filename):
    """Displays the content of a file."""
    filepath = os.path.join(REPO_PATH, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        return render_template('file.html', filename=filename, content=content)
    return "File not found", 404

@app.route('/commit/<commit_id>')
def view_commit(commit_id):
    """Displays the details of a commit."""
    commit_dir = os.path.join(REPO_PATH, ".mygit", "commits", commit_id)
    metadata_path = os.path.join(commit_dir, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return render_template('commit.html', commit_id=commit_id, metadata=metadata)
    return "Commit not found", 404

@app.route('/pull_request/create', methods=['GET', 'POST'])
def create_pull_request():
    """Creates a new pull request."""
    if request.method == 'POST':
        source_branch = request.form['source_branch']
        target_branch = request.form['target_branch']
        title = request.form['title']
        description = request.form['description']

        PULL_REQUESTS.append({
            'id': len(PULL_REQUESTS) + 1,
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title,
            'description': description,
            'status': 'open',
            'created_at': time.time(),
            'comments': []
        })

        return redirect(url_for('index'))

    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    branches = [f for f in os.listdir(branches_path) if f != "HEAD"]
    return render_template('create_pull_request.html', branches=branches)

@app.route('/pull_request/<int:pr_id>')
def view_pull_request(pr_id):
    """Displays the details of a pull request."""
    pr = next((pr for pr in PULL_REQUESTS if pr['id'] == pr_id), None)
    if pr:
        return render_template('pull_request.html', pr=pr)
    return "Pull request not found", 404

@app.route('/pull_request/<int:pr_id>/merge')
def merge_pull_request(pr_id):
    """Merges a pull request."""
    pr = next((pr for pr in PULL_REQUESTS if pr['id'] == pr_id), None)
    if pr and pr['status'] == 'open':
        merge_branches(REPO_PATH, pr['target_branch'], pr['source_branch'])
        pr['status'] = 'merged'
        pr['merged_at'] = time.time()
        return redirect(url_for('view_pull_request', pr_id=pr_id))
    return "Pull request not found or already merged", 404

# New API Endpoints

@app.route('/api/branches')
def get_branches():
    """Returns a list of branches in the repository."""
    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    branches = [f for f in os.listdir(branches_path) if f != "HEAD"]
    
    # Get current branch
    with open(os.path.join(branches_path, "HEAD"), 'r') as f:
        current_branch = f.read().strip()
    
    # Get last commit for each branch
    branch_data = []
    for branch in branches:
        branch_file = os.path.join(branches_path, branch)
        with open(branch_file, 'r') as f:
            commit_id = f.read().strip()
        
        # Get commit metadata
        commit_dir = os.path.join(REPO_PATH, ".mygit", "commits", commit_id)
        metadata_path = os.path.join(commit_dir, "metadata.json")
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            branch_data.append({
                'name': branch,
                'commit_id': commit_id,
                'last_commit_message': metadata['message'],
                'last_commit_time': metadata['timestamp'],
                'is_current': branch == current_branch
            })
    
    return jsonify({
        'branches': branch_data,
        'current_branch': current_branch
    })

@app.route('/api/commits')
def get_commits():
    """Returns a list of commits in the repository."""
    commits_path = os.path.join(REPO_PATH, ".mygit", "commits")
    commits = sorted(os.listdir(commits_path), reverse=True)
    
    commit_data = []
    for commit_id in commits:
        metadata_path = os.path.join(commits_path, commit_id, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            commit_data.append({
                'id': commit_id,
                'message': metadata['message'],
                'timestamp': metadata['timestamp'],
                'files_changed': len(metadata['files'])
            })
    
    return jsonify({'commits': commit_data})

@app.route('/api/commit/<commit_id>/message')
def get_commit_message(commit_id):
    """Returns the message of a specific commit."""
    commit_dir = os.path.join(REPO_PATH, ".mygit", "commits", commit_id)
    metadata_path = os.path.join(commit_dir, "metadata.json")
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return jsonify({'message': metadata['message']})
    
    return jsonify({'error': 'Commit not found'}), 404

@app.route('/api/file/create', methods=['POST'])
def create_file():
    """Creates a new file in the repository."""
    data = request.json
    filename = data.get('filename')
    content = data.get('content', '')
    
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400
    
    filepath = os.path.join(REPO_PATH, filename)
    
    if os.path.exists(filepath):
        return jsonify({'error': 'File already exists'}), 400
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return jsonify({'message': f'File {filename} created successfully'})

@app.route('/api/file/update', methods=['POST'])
def update_file():
    """Updates an existing file in the repository."""
    data = request.json
    filename = data.get('filename')
    content = data.get('content', '')
    
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400
    
    filepath = os.path.join(REPO_PATH, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return jsonify({'message': f'File {filename} updated successfully'})

@app.route('/api/file/delete', methods=['POST'])
def delete_file():
    """Deletes a file from the repository."""
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400
    
    filepath = os.path.join(REPO_PATH, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    os.remove(filepath)
    
    return jsonify({'message': f'File {filename} deleted successfully'})

@app.route('/api/commit/create', methods=['POST'])
def api_create_commit():
    """Creates a new commit via API."""
    data = request.json
    message = data.get('message', 'Commit via API')
    
    create_commit(REPO_PATH, message)
    
    return jsonify({'message': 'Commit created successfully'})

@app.route('/api/diff/file')
def diff_file():
    """Returns the diff of a file between two commits."""
    file_path = request.args.get('file')
    commit1 = request.args.get('commit1')
    commit2 = request.args.get('commit2', 'current')
    
    if not file_path or not commit1:
        return jsonify({'error': 'File path and commit1 are required'}), 400
    
    # Get content from first commit
    commit1_file_path = os.path.join(REPO_PATH, ".mygit", "commits", commit1, file_path)
    
    if not os.path.exists(commit1_file_path):
        return jsonify({'error': f'File not found in commit {commit1}'}), 404
    
    with open(commit1_file_path, 'r') as f:
        content1 = f.read().splitlines()
    
    # Get content from second source (either another commit or current version)
    if commit2 == 'current':
        file2_path = os.path.join(REPO_PATH, file_path)
        if not os.path.exists(file2_path):
            return jsonify({'error': 'File not found in current version'}), 404
        
        with open(file2_path, 'r') as f:
            content2 = f.read().splitlines()
    else:
        commit2_file_path = os.path.join(REPO_PATH, ".mygit", "commits", commit2, file_path)
        if not os.path.exists(commit2_file_path):
            return jsonify({'error': f'File not found in commit {commit2}'}), 404
        
        with open(commit2_file_path, 'r') as f:
            content2 = f.read().splitlines()
    
    # Generate diff
    diff = difflib.unified_diff(
        content1, 
        content2,
        fromfile=f'a/{file_path}',
        tofile=f'b/{file_path}',
        lineterm=''
    )
    
    return jsonify({'diff': '\n'.join(diff)})

@app.route('/api/diff/branch')
def diff_branch():
    """Returns the diff between two branches."""
    branch1 = request.args.get('branch1')
    branch2 = request.args.get('branch2')
    
    if not branch1 or not branch2:
        return jsonify({'error': 'Both branches are required'}), 400
    
    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    branch1_file = os.path.join(branches_path, branch1)
    branch2_file = os.path.join(branches_path, branch2)
    
    if not os.path.exists(branch1_file) or not os.path.exists(branch2_file):
        return jsonify({'error': 'One or both branches not found'}), 404
    
    with open(branch1_file, 'r') as f:
        commit1 = f.read().strip()
    
    with open(branch2_file, 'r') as f:
        commit2 = f.read().strip()
    
    # Get files in both commits
    commit1_dir = os.path.join(REPO_PATH, ".mygit", "commits", commit1)
    commit2_dir = os.path.join(REPO_PATH, ".mygit", "commits", commit2)
    
    commit1_metadata_path = os.path.join(commit1_dir, "metadata.json")
    commit2_metadata_path = os.path.join(commit2_dir, "metadata.json")
    
    with open(commit1_metadata_path, 'r') as f:
        commit1_metadata = json.load(f)
    
    with open(commit2_metadata_path, 'r') as f:
        commit2_metadata = json.load(f)
    
    commit1_files = set(commit1_metadata['files'].keys())
    commit2_files = set(commit2_metadata['files'].keys())
    
    all_files = commit1_files.union(commit2_files)
    added_files = commit2_files - commit1_files
    removed_files = commit1_files - commit2_files
    modified_files = []
    
    for file in commit1_files.intersection(commit2_files):
        if commit1_metadata['files'][file] != commit2_metadata['files'][file]:
            modified_files.append(file)
    
    # Prepare response with file status
    files_data = []
    
    for file in all_files:
        status = 'added' if file in added_files else 'removed' if file in removed_files else 'modified' if file in modified_files else 'unchanged'
        
        files_data.append({
            'name': file,
            'status': status
        })
    
    return jsonify({
        'branch1': branch1,
        'branch2': branch2,
        'commit1': commit1,
        'commit2': commit2,
        'files': files_data,
        'summary': {
            'total': len(all_files),
            'added': len(added_files),
            'removed': len(removed_files),
            'modified': len(modified_files)
        }
    })

@app.route('/api/branch/create', methods=['POST'])
def create_branch_api():
    """Creates a new branch via API."""
    data = request.json
    branch_name = data.get('name')
    source_branch = data.get('source_branch', 'main')
    
    if not branch_name:
        return jsonify({'error': 'Branch name is required'}), 400
    
    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    
    if os.path.exists(os.path.join(branches_path, branch_name)):
        return jsonify({'error': f'Branch {branch_name} already exists'}), 400
    
    source_branch_file = os.path.join(branches_path, source_branch)
    
    if not os.path.exists(source_branch_file):
        return jsonify({'error': f'Source branch {source_branch} not found'}), 404
    
    with open(source_branch_file, 'r') as f:
        commit_id = f.read().strip()
    
    with open(os.path.join(branches_path, branch_name), 'w') as f:
        f.write(commit_id)
    
    return jsonify({'message': f'Branch {branch_name} created successfully'})

@app.route('/api/branch/switch', methods=['POST'])
def switch_branch_api():
    """Switches to a different branch via API."""
    data = request.json
    branch_name = data.get('name')
    
    if not branch_name:
        return jsonify({'error': 'Branch name is required'}), 400
    
    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    branch_file = os.path.join(branches_path, branch_name)
    
    if not os.path.exists(branch_file):
        return jsonify({'error': f'Branch {branch_name} not found'}), 404
    
    with open(branch_file, 'r') as f:
        commit_id = f.read().strip()
    
    # Revert to the branch's commit
    revert_to_commit(REPO_PATH, commit_id)
    
    # Update HEAD
    with open(os.path.join(branches_path, "HEAD"), 'w') as f:
        f.write(branch_name)
    
    return jsonify({'message': f'Switched to branch {branch_name}'})

@app.route('/branches')
def branches_page():
    """Displays the branches page."""
    branches_path = os.path.join(REPO_PATH, ".mygit", "branches")
    branches = [f for f in os.listdir(branches_path) if f != "HEAD"]
    
    # Get current branch
    with open(os.path.join(branches_path, "HEAD"), 'r') as f:
        current_branch = f.read().strip()
    
    return render_template('branches.html', branches=branches, current_branch=current_branch)

@app.route('/pull_request/<int:pr_id>/comment', methods=['POST'])
def add_pr_comment(pr_id):
    """Adds a comment to a pull request."""
    pr = next((pr for pr in PULL_REQUESTS if pr['id'] == pr_id), None)
    if not pr:
        return jsonify({'error': 'Pull request not found'}), 404
    
    data = request.json
    comment = data.get('text')
    
    if not comment:
        return jsonify({'error': 'Comment text is required'}), 400
    
    if 'comments' not in pr:
        pr['comments'] = []
    
    pr['comments'].append({
        'id': len(pr['comments']) + 1,
        'text': comment,
        'author': 'User',  # In a real app, this would be the current user
        'timestamp': time.time()
    })
    
    return jsonify({'message': 'Comment added successfully'})

@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """Converts a timestamp to a human-readable date."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

if __name__ == '__main__':
    os.makedirs(REPO_PATH, exist_ok=True)
    init_repository(REPO_PATH)
    app.run(debug=True)

# Example usage
repo_path = "my_repo"
os.makedirs(repo_path, exist_ok=True)
init_repository(repo_path)

with open(os.path.join(repo_path, "example.txt"), 'w') as f:
    f.write("Initial content\n")

create_commit(repo_path, "Initial commit")

create_branch(repo_path, "feature-branch")

with open(os.path.join(repo_path, "example.txt"), 'a') as f:
    f.write("Added a line to main\n")

create_commit(repo_path, "added line to main")

switch_branch(repo_path, "feature-branch")

with open(os.path.join(repo_path, "example.txt"), 'a') as f:
    f.write("Added a different line to feature branch\n")

create_commit(repo_path, "added different line to feature branch")

switch_branch(repo_path, "main")

merge_branches(repo_path, "main", "feature-branch")