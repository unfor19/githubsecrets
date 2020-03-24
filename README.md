# github-secrets

Manage your [GitHub Actions](https://github.com/features/actions) secrets, with a simple Python script

![Usage-Example](./assets/github-secrets-usage.gif)

## Getting Started

### Authentication

#### Auth methods
Available authentication methods, ordered by precedence

1. OAuth Token - [Personal Access Token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
2. Username and Password

#### Auth arguments
Available authentication arguments, ordered by precedence
1. Environment Variables
   - GITHUB_USERNAME
   - GITHUB_PASSWORD
   - GITHUB_ORGANIZATION
   - GITHUB_OAUTH_TOKEN
2. Creds File - create a file `.github_creds.json`, and execute this app from the same directory
    ```
    {
       "GITHUB_USERNAME": "",
       "GITHUB_PASSWORD": "",
       "GITHUB_ORGANIZATION": "",
       "GITHUB_OAUTH_TOKEN": ""
    }
    ```

### Usage

#### Available ACTIONs
```
apply  - create or update, returns 204
get    - returns 200
delete - returns 204
list   - returns 200
help
```

#### Using Shell
Download the file - [github-secrets.py](https://raw.githubusercontent.com/unfor19/github-secrets/master/github-secrets.py)

##### Environment Variables

```bash
$ export GITHUB_USERNAME=my_username GITHUB_PASSWORD=my_password GITHUB_ORGANIZATION=my_organization
$ python3 github-actions.py ACTION REPO_NAME [SECRET_NAME] [SECRET_VALUE]
```
##### Creds File

```bash
$ python3 github-actions.py ACTION REPO_NAME [SECRET_NAME] [SECRET_VALUE]
```

#### Using Docker (will be ready soon)
```bash
$ docker run --rm \
    -v ./.github_secrets.json:/code/.github_creds.json \
    -e GITHUB_USERNAME=my_username \
    -e GITHUB_PASSWORD=my_password \
    -e GITHUB_ORGANIZATION=my_organization \
    -e GITHUB_OAUTH_TOKEN=my_oauth_token \
    unfor19/github-secrets ACTION REPO_NAME [SECRET_NAME] [SECRET_VALUE]
```
