from pathlib import Path
from os import path, mkdir
import json
import click


def error_exit(msg):
    click.echo(msg)
    exit()


def create_artifacts():
    config = Config(raise_error=False)
    artifacts = config.deserialize()['artifacts']
    for key, artifact in artifacts.items():
        if not artifact['exists']:
            if artifact['type'] == "file":
                with open(artifact['path'], 'w') as file:
                    file.write('')
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
            with open(config.credentials, 'r') as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = ''

        return data

    @staticmethod
    def set_credentials_content(credentials_content):
        config = Config()
        with open(config.credentials, 'w') as file:
            json.dump(credentials_content, file)
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
