# githubsecrets

![Release Version](https://img.shields.io/github/v/release/unfor19/githubsecrets) [![Build Status](https://cloud.drone.io/api/badges/unfor19/githubsecrets/status.svg)](https://cloud.drone.io/unfor19/githubsecrets) ![Open Issues](https://img.shields.io/github/issues-raw/unfor19/githubsecrets) ![PyPi Downloads](https://img.shields.io/pypi/dm/githubsecrets) ![License MIT](https://img.shields.io/github/license/unfor19/githubsecrets)

A simple CLI to manage GitHub secrets, that are used with [GitHub Actions](https://github.com/features/actions)

![Usage-Example](./assets/github-secrets-usage.gif)

## Installation

### pip

Python v3.6.7 and above

Install with pip on your machine; the package is available at [PyPi](https://pypi.org/project/githubsecrets/)

```bash
$ pip install githubsecrets
```

### Docker

Mount your home directory to `root`, the image is available at [DockerHub](https://hub.docker.com/r/unfor19/githubsecrets)

The image runs as a CLI; you must provide arguments, prompts are not available while running in Docker

```bash

# available commands
$ docker run -v $HOME:/root unfor19/githubsecrets --help
Usage: ghs [OPTIONS] COMMAND [ARGS]...
...

# create credentials file
$ docker run --rm -v $HOME:/root unfor19/githubsecrets init
```

### Build

You can easily build from source with
```bash
$ git clone https://github.com/unfor19/githubsecrets.git && cd githubsecrets
...
$ pip install --upgrade pip
...
$ pip install -r requirements.txt
...
$ pip install --editable .
...
# Done!
```

## Getting Started

1. Initialize this application - Creates a credential file at `~/.githubsecrets/credentials`

   ```bash
   $ ghs init
   ```

1. [Generate a GitHub Personal-Access-Token](https://github.com/settings/tokens) with the following permssions:

   - repo (all)
   - admin:public_key > read:public_key

1. Save the token in a safe place; we'll use it in the next step

1. Create a profile, use the `-p` flag and supply a profile name

   ```bash
   $ ghs profile-apply -p willy_wonka
   ...
   SUCCESS: Applied the profile willy_wonka
   ```

   You'll be prompted to insert:

   - Github owner - which is your GitHub Organization or GitHub Account name (not email address)
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

### Available commands

View all available commands with `ghs --help`

```
Usage: ghs [OPTIONS] COMMAND [ARGS]...

All commands can run without providing options, and then you'll be
prompted to insert values.

Secrets' values and Personal-Access-Tokens are hidden when prompted

Options:
--help Show this message and exit.

Commands:
init Create a credentials file to store your profiles
profile-apply Create or modify a profile
profile-delete Delete a profile
profile-list List all profile - truncates personal access tokens
secret-apply Create or modify a secret in a GitHub repository
secret-delete Delete a secret in a GitHub repository
secret-get Get a secret from a GitHub repository
secret-list List all secret in a GitHub repository
```

## Contributing

Report issues/questions/feature requests on in the [Issues](https://github.com/unfor19/githubsecrets/issues) section.

Pull requests are welcome! Ideally, create a feature branch and issue for every single change you make. These are the steps:

1. Fork this repo
2. Create your feature branch from master (`git checkout -b my-new-feature`)
3. Commit your remarkable changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push --set-up-stream origin my-new-feature`)
5. Create a new Pull Request and tell us about your changes

## Authors

Created and maintained by [Meir Gabay](https://github.com/unfor19)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/unfor19/githubsecrets/blob/master/LICENSE) file for details
