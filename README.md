
# GitHub Repository Tracker

## Overview
This Python script provides a robust solution for tracking GitHub repositories. It efficiently fetches and analyzes repository data for a list of users, offering insights into both public and private repositories. Ideal for monitoring changes and growth in GitHub profiles.

## Features
- Fetches user repositories using GitHub's API.
- Filters and lists public repositories for each user.
- Counts private repositories, maintaining user privacy.
- Tracks new public repositories since the last script run.
- Generates a comprehensive summary of repository statistics.

## Prerequisites
- Python 3.x
- `requests` library
- `json` library
- `time` library
- `keyring` library

## Setup
1. **Install Required Libraries**: Ensure all required Python libraries are installed:
   ```bash
   pip install requests keyring
   ```
2. **GitHub Token**: Securely store your GitHub token in the keyring:
   ```python
   keyring.set_password("github", "your-username", "your-token")
   ```

## Usage
1. **Prepare User List**: Populate 'usernames.txt' with GitHub usernames, one per line.
2. **Run the Script**: Execute the script via the command line:
   ```bash
   python script_name.py
   ```

## Output
- Terminal output displaying the processing progress and summary.
- A 'stored_data.json' file containing the current state of tracked repositories.

## Limitations
- Rate limiting by GitHub's API may require adjusting the sleep timer in the script.
- Handles only public and private repositories (no distinctions for forks, gists, etc.).
