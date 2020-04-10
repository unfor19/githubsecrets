# github-secrets

A simple CLI to manage GitHub secrets, that are used with [GitHub Actions](https://github.com/features/actions)

![Usage-Example](./assets/github-secrets-usage.gif)

## Installation

```bash
$ pip install githubsecrets
```

## Getting Started

1. Initialize this application to create a credentials file
   ```bash
   $ ghs init
   ```
1. [Create a GitHub Personal-Access-Token](https://github.com/settings/tokens) with the following permssions:
   1. repo (all)
   1. admin:public_key > read:public_key
1. Save the token in a safe place, we'll use it in a second
1. Create a profile
   ```bash
   $ ghs profile-apply -p willy_wonka
   ...
   SUCCESS: Applied the profile willy_wonka
   ```
   You'll be prompted to insert:
   - Github owner- which is your GitHub Organization or GitHub Account name
   - Personal access token - that you've created in the previous steps
1. Create a GitHub secret
   ```bash
   ghs secret-apply -p willy_wonka -r github-secrets
   ```
   You'll be prompted to insert:
   - Secret name
   - Secret value

### Status codes

- 200 - success
- 204 - success
- 404 - secret or repository not found
