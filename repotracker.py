import requests
import json
import time
import keyring

def get_public_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching repos for user {username}: {response.status_code}")
        print("Rate Limit Status:", response.headers.get('X-RateLimit-Remaining'))
        return [], 0  # Ensure two values are returned

    try:
        repos = response.json()
        if not isinstance(repos, list):
            raise ValueError("Unexpected response format")
        public_repos = [repo['name'] for repo in repos if not repo['private']]
        private_count = len([repo for repo in repos if repo['private']])
        return public_repos, private_count
    except ValueError as e:
        print(f"Error parsing repos for user {username}: {e}")
        return [], 0  # Ensure two values are returned

def load_usernames(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def load_stored_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_stored_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

def print_summary(user_stats, total_private_repos, total_public_repos, previous_data):
    print("\n=== Repository Summary ===")
    for user, stats in user_stats.items():
        previous_public_repos = len(previous_data.get(user, []))
        change_in_public_repos = stats['public'] - previous_public_repos
        print(f"User: {user}, Public Repos: {stats['public']} (Change: {change_in_public_repos}), New Public Repos: {len(stats['new'])}")

    print(f"Total Public Repositories: {total_public_repos}")
    print(f"Total Private Repositories Discovered: {total_private_repos}")

def main():
    # Replace 'your-username' with your GitHub username and ensure your token is stored in keyring
    github_token = keyring.get_password("github", "your-username")
    
    if not github_token:
        raise ValueError("GitHub token not found in keyring")

    # Replace 'usernames.txt' with your file containing GitHub usernames
    usernames = load_usernames('usernames.txt')
    stored_data = load_stored_data('stored_data.json')

    user_stats = {}
    total_private_repos = 0
    total_public_repos = 0

    total_users = len(usernames)
    previous_data = load_stored_data('stored_data.json')

    for index, username in enumerate(usernames, start=1):
        print(f"Processing user {index} of {total_users}: {username}...")

        current_repos, private_count = get_public_repos(username, github_token)
        public_repos_count = len(current_repos)
        total_public_repos += public_repos_count
        total_private_repos += private_count

        stored_repos = stored_data.get(username, [])
        new_repos = set(current_repos) - set(stored_repos)

        if new_repos:
            print(f"\nNew public repos for {username}:")
            for repo in new_repos:
                print(f"  - {repo}")

        user_stats[username] = {'public': public_repos_count, 'new': list(new_repos)}

        stored_data[username] = current_repos
        time.sleep(1)  # Adjust this as needed to respect rate limits

    save_stored_data('stored_data.json', stored_data)
    print_summary(user_stats, total_private_repos, total_public_repos, previous_data)

if __name__ == "__main__":
    main()
