# MyGit - Git-like Version Control System

MyGit is a web-based Git-like version control system built with Python and Flask. It provides a modern, intuitive UI for managing repositories, branches, commits, and pull requests, similar to platforms like GitHub but running locally.

![MyGit Screenshot](screenshot.png)

## Features

- **Repository Management**: Initialize and manage local repositories.
- **File Management**: Create, edit, delete, and commit files with a web-based editor.
- **Version Control**: Track changes with commit history and visualizations.
- **Branching**: Create, switch, and manage multiple branches.
- **Branch Comparison**: Compare branches and visualize differences.
- **Pull Requests**: Create, review, and merge pull requests with comments.
- **Diff Viewer**: Visualize file changes with a side-by-side diff view.
- **Modern UI**: Responsive, intuitive interface built with Tailwind CSS.

## Setup Instructions

### Prerequisites

- Python 3.7+
- Flask

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/mygit.git
   cd mygit
   ```

2. Install dependencies:

   ```
   pip install flask
   ```

3. Run the application:

   ```
   python mygit.py
   ```

4. Access the web interface:
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `mygit.py`: Core application logic and Flask routes
- `templates/`: HTML templates for the web interface
  - `base.html`: Base template with common layout
  - `index.html`: Repository dashboard
  - `file.html`: File viewer and editor
  - `commit.html`: Commit details and diff viewer
  - `branches.html`: Branch management
  - `pull_request.html`: Pull request details
  - `create_pull_request.html`: Pull request creation form

## How It Works

### Core Concepts

- **Repository**: A directory containing all your project files and the `.mygit` subdirectory.
- **Commit**: A snapshot of your repository at a specific point in time.
- **Branch**: A movable pointer to a specific commit, allowing parallel development.
- **Pull Request**: A request to merge changes from one branch into another, with review capabilities.

### Workflow

1. **Initialize Repository**: Creates a `.mygit` directory with necessary data structures.
2. **Make Changes**: Create, edit, or delete files in the repository.
3. **Commit Changes**: Save snapshots of files with commit messages.
4. **Create Branches**: Branch off from main for new features or bug fixes.
5. **Create Pull Requests**: Request to merge your branch changes into another branch.
6. **Review and Merge**: Review changes and merge them when ready.

## API Endpoints

The application provides several API endpoints for programmatic access:

- `/api/branches`: Get all branches
- `/api/commits`: Get all commits
- `/api/commit/<commit_id>/message`: Get commit message
- `/api/file/create`: Create a new file
- `/api/file/update`: Update file content
- `/api/file/delete`: Delete a file
- `/api/commit/create`: Create a new commit
- `/api/diff/file`: Get file diff between commits
- `/api/diff/branch`: Get diff between branches
- `/api/branch/create`: Create a new branch
- `/api/branch/switch`: Switch to a different branch
- `/api/pull_request/<pr_id>/comment`: Add a comment to a pull request

## Technical Implementation

- **File Storage**: Files are stored directly in the repository directory, with commit snapshots stored in `.mygit/commits/`.
- **Branching**: Branch information is stored in `.mygit/branches/` with pointers to commits.
- **Diffs**: Generated using Python's `difflib` for comparing file versions.
- **Web Interface**: Built with Flask for the backend and Tailwind CSS for the frontend.
- **Interactive Elements**: Uses JavaScript for dynamic behavior and visualization.

## Future Enhancements

- User authentication and authorization
- Remote repository synchronization
- Git compatibility layer
- Enhanced search functionality
- Webhook integration
- CI/CD pipeline integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Git and GitHub
- Built with Flask and Tailwind CSS
- Diff visualization powered by diff2html.js
- Chart visualization powered by Chart.js
