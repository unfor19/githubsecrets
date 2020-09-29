# githubsecrets

[![testing](https://github.com/unfor19/githubsecrets/workflows/testing/badge.svg)](https://github.com/unfor19/githubsecrets/actions?query=workflow%3Atesting)

<img width="100%" alt="GithubSecrets-Website" src="https://githubsecrets.s3-eu-west-1.amazonaws.com/githubsecrets-website-gradient.png" />

Manage your [GitHub Actions](https://github.com/features/actions) secrets, with a simple CLI

<details><summary>
GIF Demo
</summary>
 
![Usage-Demo](https://githubsecrets.s3-eu-west-1.amazonaws.com/githubsecrets-demo.gif)

</details>

## Installation

### pip

Python v3.6.7 and above

Install with pip on your machine; the package is available at [PyPi](https://pypi.org/project/githubsecrets/)

```bash
$ pip install githubsecrets
```

### Ubuntu and Debian

This project uses the [keyring](https://pypi.org/project/keyring/) package, in some versions of Ubuntu and Debian, you might need to install the following packages

```
$ sudo apt-get update && sudo apt-get install -y libdbus-glib-1-dev
$ pip install secretstorage dbus-python keyring
```

### Docker

<details><summary>Expand/Collapse
 </summary>

Mount a local directory to `root`, the image is available at [DockerHub](https://hub.docker.com/r/unfor19/githubsecrets)

#### Linux and macOS

Mount your home directory, or any other directory to save the credentials file

```bash
$ docker run --rm -it -v "${HOME}/:/root" unfor19/githubsecrets secret-list -p unfor19 -r githubsecrets
... # Output below
```

<details><summary>Output
</summary>

```json
[
  {
    "base_url": "https://api.github.com/repos/unfor19/githubsecrets",
    "body": {
      "secrets": [
        {
          "created_at": "2020-04-11T00:01:12Z",
          "name": "PIP_PASSWORD",
          "updated_at": "2020-04-11T00:17:39Z"
        },
        {
          "created_at": "2020-04-10T23:21:28Z",
          "name": "PIP_USERNAME",
          "updated_at": "2020-04-11T00:17:20Z"
        },
        {
          "created_at": "2020-04-27T20:44:09Z",
          "name": "testing",
          "updated_at": "2020-04-27T20:45:43Z"
        },
        {
          "created_at": "2020-04-27T20:22:37Z",
          "name": "testrepos",
          "updated_at": "2020-04-27T20:22:37Z"
        },
        {
          "created_at": "2020-04-14T14:14:44Z",
          "name": "TEST_GITHUB_TOKEN",
          "updated_at": "2020-04-14T14:14:44Z"
        }
      ],
      "total_count": 5
    },
    "repository": "githubsecrets",
    "status_code": 200
  }
]
```

</details>

#### Windows

Mount your Temp directory, or any other directory to save the credentials file. Make sure you use `/` and not `\`

```
$ docker run --rm -it -v c:/Temp:/root unfor19/githubsecrets secret-delete -p unfor19 -r githubsecrets -s testrepos
... # Output below
```

<details><summary>Output
</summary>

```json
[
  {
    "base_url": "https://api.github.com/repos/unfor19/githubsecrets",
    "repository": "githubsecrets",
    "secret_name": "testrepos",
    "status_code": 204
  }
]
```

</details>

</details>

## Getting Started

**Note**: When using Docker, no need to add `ghs`; supply only a command and its arguments

1. Initialize this application - Creates a credentials file at `~/.githubsecrets/credentials`

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

1. Create a GitHub secret, use the `-r` flag and supply the repository's name. You can apply the same secret to multiple repositories at once, for example: `-r "githubsecrets, aws-build-badges"`

   ```bash
   ghs secret-apply -p willy_wonka -r githubsecrets
   ```

   You'll be prompted to insert:

   - Secret name
   - Secret value

1. Use it in your [GitHub Actions Workflows](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions)
   - Snippet
     ```yml
     steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: "3.6"
      - name: Install dependencies
        run: |
          ...
      - name: Build and publish
        env:
          TWINE_USERNAME: ${{ secrets.PIP_USERNAME }}
          TWINE_PASSWORD: ${{ secrets.PIP_PASSWORD }}
          ...
        run: |
          ...
     ```
   - I'm using secrets in this repository, check out [this repository's workflows](https://github.com/unfor19/githubsecrets/tree/master/.github/workflows)

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
  -ci, --ci  Use this flag to avoid deletion confirmation prompts
  --help     Show this message and exit.

Commands:
  init            Create a credentials file to store your profiles
  profile-apply   Create or modify multiple profiles providing a string...
  profile-delete  Delete multiple profiles providing a string delimited by...
  profile-list    List all profile - truncates personal access tokens
  secret-apply    Apply to multiple repositories providing a string...
  secret-delete   Delete secrets from multiple repositories providing a...
  secret-get      Get secrets from multiple repositories providing a string...
  secret-list     List secrets of multiple repositories providing a string...
```

## Contributing

Report issues/questions/feature requests on the [Issues](https://github.com/unfor19/githubsecrets/issues) section.

Pull requests are welcome! Ideally, create a feature branch and issue for every single change you make. These are the steps:

1. Fork this repo
1. Create your feature branch from master (`git checkout -b my-new-feature`)
1. Install from source
   ```bash
    $ git clone https://github.com/${GITHUB_OWNER}/githubsecrets.git && cd githubsecrets
    ...
    $ pip install --upgrade pip
    ...
    $ python -m venv ./ENV
    $ . ./ENV/bin/activate
    ...
    $ (ENV) pip install --editable .
    ...
    # Done! Now when you run 'ghs' it will get automatically updated when you modify the code
   ```
1. Add the code of your new feature
1. Test - generate a Personal Access Token for testing
   ```bash
   $ (ENV) bash test_functionality.sh -p PROFILE_NAME -o GITHUB_OWNER -t TEST_GITHUB_TOKEN -r GITHUB_REPOSITORY
   ... # All good? Move on to the next step
   ```
1. Commit your remarkable changes (`git commit -am 'Added new feature'`)
1. Push to the branch (`git push --set-up-stream origin my-new-feature`)
1. Create a new Pull Request and tell us about your changes

## Authors

Created and maintained by [Meir Gabay](https://github.com/unfor19)

Design by [facebook.com/KerenOrDesign](https://facebook.com/KerenOrDesign)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/unfor19/githubsecrets/blob/master/LICENSE) file for details
