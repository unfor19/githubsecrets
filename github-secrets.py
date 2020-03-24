import os
import sys
import requests
import json
from base64 import b64encode
from nacl import encoding, public

# Reference: https://developer.github.com/v3/actions/secrets/


def usage():
    """Print usage and exit"""

    print("""
    Available ACTIONs
    =================
    apply  - create or update, returns 204
    get    - returns 200, and the name of the secret
    delete - returns 204
    list   - returns 200, and the list of available secrets

    Using Shell
    ===========
    $ GITHUB_ORGANIZATION=my_organization export GITHUB_USERNAME=my_username GITHUB_PASSWORD=my_password
    $ python3 github-actions.py ACTION REPO_NAME [SECRET_NAME] [SECRET_VALUE]

    Using Docker
    ============
    $ docker run --rm \\
        -v ./.github_secrets.json:/code/.github_creds.json \\
        -e GITHUB_ORGANIZATION=my_organization \\        
        -e GITHUB_OAUTH_TOKEN=my_oauth_token \\
        -e GITHUB_USERNAME=my_username \\
        -e GITHUB_PASSWORD=my_password \\
        unfor19/github-secrets ACTION REPO_NAME [SECRET_NAME] [SECRET_VALUE]
    """)
    exit()


def encrypt(public_key: str, secret_value: str) -> str:
    """
    Encrypt a Unicode string using the public key. \n
    Source: https://developer.github.com/v3/actions/secrets/#example-encrypting-a-secret-using-python
    """
    public_key = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def request(method, args_dict, api_path, parameters={}) -> requests.request:
    full_url = f"{args_dict['base_url']}/{api_path}"
    if args_dict['github_credentials']['GITHUB_OAUTH_TOKEN']:
        # Using OAUTH Token
        headers = { 'Authorization': f"token {args_dict['github_credentials']['GITHUB_OAUTH_TOKEN']}" }
        req = requests.request(
            method,
            url=full_url,
            json=parameters,
            headers=headers
        )
    elif args_dict['github_credentials']['GITHUB_USERNAME'] and args_dict['github_credentials']['GITHUB_PASSWORD']:
        # Using Username and Password
        req = requests.request(
            method,
            url=full_url,
            json=parameters,
            auth=(
                args_dict['github_credentials']['GITHUB_USERNAME'],
                args_dict['github_credentials']['GITHUB_PASSWORD']
            )
        )
    else:
        raise Exception('Did not supply credentials')
    return req


def read_creds() -> dict:
    """Reads credentials from Environment Variables, if fails, tries from Creds file"""
    required_args = [
        'GITHUB_ORGANIZATION',
    ]

    creds = {}
    use_creds_file = False

    # Using environment variables
    for arg in required_args:
        if not arg in os.environ or not os.environ[arg]:
            use_creds_file = True
            break
        creds[arg] = os.environ[arg]

    # Using credentials file
    if use_creds_file:
        creds_file_name = '.github_creds.json'
        if not os.path.exists(creds_file_name):
            raise Exception(
                f"No environment variables, and the file {creds_file_name} doesn't exist"
            )

        with open('.github_creds.json') as f:
            creds = json.load(f)

        for arg in required_args:
            if not arg in creds:
                raise Exception(f"{arg} is not in .env.json")

    return creds


def get_public_key(args_dict) -> requests.request:
    """Get the repository's public key, used when creating/updating a secret"""
    return request('get', args_dict, 'actions/secrets/public-key')


def get_secret(args_dict) -> requests.request:
    """Get a secret"""
    return request(
        'get',
        args_dict,
        f"actions/secrets/{args_dict['secret_name']}"
    )


def apply_secret(args_dict) -> requests.request:
    """Create or update a secret"""
    public_key = get_public_key(args_dict)
    if public_key.status_code >= 300 or public_key.status_code < 200:
        raise Exception(public_key.text)
    else:
        public_key = public_key.json()
    encrypted_value = encrypt(public_key['key'], args_dict['secret_value'])

    parameters = {
        "encrypted_value": encrypted_value,
        "key_id": public_key['key_id']
    }

    return request(
        'put',
        args_dict,
        f"actions/secrets/{args_dict['secret_name']}",
        parameters=parameters
    )


def list_secrets(args_dict) -> requests.request:
    """Lists all secrets in repository"""
    return request(
        'get',
        args_dict,
        f"actions/secrets"
    )


def delete_secret(args_dict) -> requests.request:
    """Delete a secret"""
    return request(
        'delete',
        args_dict,
        f"actions/secrets/{args_dict['secret_name']}"
    )


def print_response(response):
    """Prints a human-readable response"""
    res = {}
    if (response.text):
        try:
            res['body'] = response.json()
        except:
            res['body'] = response.text
    res['status_code'] = response.status_code
    print(json.dumps(res, indent=4, sort_keys=True))


def main():
    available_actions = [
        'apply',
        'get',
        'delete',
        'list',
        'help'
    ]

    args_structure = {
        "0": "action",
        "1": "repo_name",
        "2": "secret_name",
        "3": "secret_value"
    }

    args = sys.argv[1:] # Reads given arguments from terminal
    args_dict = {}
    for (i, value) in enumerate(args):
        secret_name = args_structure[str(i)]
        args_dict[secret_name] = value

    if not args_dict['action'] in available_actions:
        raise Exception('Unknown ACTION')

    if args_dict['action'] == 'help':
        usage()

    args_dict['github_credentials'] = read_creds()
    args_dict['base_url'] = f"https://api.github.com/repos/{args_dict['github_credentials']['GITHUB_ORGANIZATION']}/{args_dict['repo_name']}"

    if args_dict['action'] == 'apply':
        response = apply_secret(args_dict)
    elif args_dict['action'] == 'get':
        response = get_secret(args_dict)
    elif args_dict['action'] == 'list':
        response = list_secrets(args_dict)
    elif args_dict['action'] == 'delete':
        response = delete_secret(args_dict)

    print_response(response)


if __name__ == "__main__":
    main()
