from pathlib import Path
from os import path, mkdir
import json
import click
from cryptography.fernet import Fernet
import keyring
import os


def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def print_pretty_json(res):
    click.echo(json.dumps(res, indent=4, sort_keys=True))


def list_by_comma(my_string):
    return [item.strip() for item in my_string.split(",")]


def error_exit(msg):
    click.echo(msg)
    exit()


def get_encryption_hash():
    secret_hash = keyring.get_password("githubsecrets", "secret_hash")
    if secret_hash:
        return secret_hash.encode()
    else:
        return None


def encrypt_data(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(data, str):
        error_exit("ERROR: Cannot encrypt non-strings")
    encoded = data.encode()
    fernet = Fernet(get_encryption_hash())
    return fernet.encrypt(encoded)


def decrypt_data(encrypted):
    fernet = Fernet(get_encryption_hash())
    decrypted = fernet.decrypt(encrypted)
    try:
        decrypted = json.loads(decrypted)
    except:  # noqa: E722
        pass
    return decrypted


def create_artifacts(config):
    config.raise_error = False
    artifacts = config.deserialize()['artifacts']
    current_hash = get_encryption_hash()
    if not current_hash:
        secret_hash = Fernet.generate_key().decode()
        keyring.set_password("githubsecrets", "secret_hash", secret_hash)

    for key, artifact in artifacts.items():
        if not artifact['exists']:
            if artifact['type'] == "file":
                with open(artifact['path'], 'wb') as file:
                    file.write(encrypt_data(''))
                click.echo(f"Created file - {artifact['path']}")
            elif artifact['type'] == "dir":
                mkdir(artifact['path'])
                click.echo(f"Created dir - {artifact['path']}")
            else:
                raise Exception("Unknown artifact type")
        else:
            click.echo(
                f"{artifact['type'].title()} exists - {artifact['path']}"
            )


class Config(object):
    def __init__(self, raise_error=True):
        self.verbose = False
        self.home_dir = f"{Path.home()}"
        self.ghs_dir = f"{self.home_dir}/.githubsecrets"
        self.credentials = f"{self.ghs_dir}/credentials"
        self.errors = 0
        self.errors_msg = ""
        # self.validate(raise_error)
        self.ci = False

    @staticmethod
    def get_credentials_content():
        config = Config()
        try:
            with open(config.credentials, 'rb') as file:
                encrypted = file.read()
            data = decrypt_data(encrypted)
        except json.decoder.JSONDecodeError:
            data = ''

        return data

    @staticmethod
    def set_credentials_content(credentials_content):
        config = Config()
        encrypted = encrypt_data(credentials_content)
        with open(config.credentials, 'wb') as file:
            file.write(encrypted)
        return True

    @staticmethod
    def print_response(response):
        """Prints a human-readable response"""
        res = {}
        if (response.text):
            try:
                res['body'] = response.json()
            except:  # noqa: E722
                res['body'] = response.text
        res['status_code'] = response.status_code
        print(json.dumps(res, indent=4, sort_keys=True))

    def deserialize(self):
        return {
            "artifacts": {
                "ghs_dir": {
                    "path": self.ghs_dir,
                    "type": "dir",
                    "exists": path.isdir(self.ghs_dir)
                },
                "credentials": {
                    "path": self.credentials,
                    "type": "file",
                    "exists": path.isfile(self.credentials)
                },
            },
            "errors": self.errors,
            "errors_msg": self.errors_msg
        }

    def validate(self, raise_error):
        artifacts = self.deserialize()['artifacts']
        self.errors_msg = "\nERROR: Missing files/folders\n"
        for key, artifact in artifacts.items():
            if not artifact['exists']:
                self.errors_msg += f"{artifact['path']}\n"
                self.errors += 1

        if self.errors > 0 and raise_error:
            self.errors_msg += "Fix it by executing: ghs init\n"
            error_exit(self.errors_msg)


class Validate(object):
    def __init__(self, raise_error=True):
        config = Config()
        artifacts = config.deserialize()['artifacts']
        config.errors_msg = "\nERROR: Missing files/folders\n"
        for key, artifact in artifacts.items():
            if not artifact['exists']:
                config.errors_msg += f"{artifact['path']}\n"
                config.errors += 1

        if config.errors > 0 and raise_error:
            config.errors_msg += "Fix it by executing: ghs init\n"
            error_exit(config.errors_msg)


pass_config = click.make_pass_decorator(Config, ensure=True)
pass_validate = click.make_pass_decorator(Validate, ensure=True)
