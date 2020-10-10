import click
from .config import Config, error_exit


class Profile():
    def __init__(self, config, name):
        self.name = name
        self.credentials_content = Config.get_credentials_content()
        self.github_owner = ''
        self.personal_access_token = ''
        self.config = config
        if self.credentials_content and self.name in self.credentials_content:
            self.github_owner = self.credentials_content[self.name]['github_owner']  # noqa: E501
            self.personal_access_token = self.credentials_content[self.name]['personal_access_token']  # noqa: E501

    @staticmethod
    def lista():
        credentials_content = Config.get_credentials_content()
        msg = "\n"
        if not credentials_content:
            error_exit(
                "WARNING: Couldn't find any profile, create one by executing:\nghs profile-apply -p profile_name\n")  # noqa: E501
        for key, value in credentials_content.items():
            token_length = len(value['personal_access_token'])
            value['personal_access_token'] = \
                value['personal_access_token'][0:7] + \
                "*" * (token_length - 8)
            msg += f"profile: {key}, github_owner: {value['github_owner']}, personal_access_token: {value['personal_access_token']}\n"  # noqa: E501
        click.echo(msg)

    def apply(self, github_owner, personal_access_token):
        if self.credentials_content:
            self.credentials_content[self.name] = {
                "github_owner": github_owner,
                "personal_access_token": personal_access_token
            }
        else:
            self.credentials_content = {
                self.name: {
                    "github_owner": github_owner,
                    "personal_access_token": personal_access_token
                }
            }

        write_success = Config.set_credentials_content(
            self.credentials_content
        )
        if write_success:
            click.echo(f"SUCCESS: Applied the profile {self.name}")
        else:
            click.echo(f"FAILED: Unable to create the profile {self.name}")

    def get(self):
        pass

    def delete(self):
        if self.name in self.credentials_content:
            del self.credentials_content[self.name]
            confirm = False
            if self.config.ci:
                confirm = True
            elif click.confirm(f"Are you sure want to delete the profile {self.name} ?"):  # noqa: E501
                confirm = True

            if confirm:
                write_success = Config.set_credentials_content(
                    self.credentials_content)
                if write_success:
                    click.echo(f"SUCCESS: Deleted the profile {self.name}")
                else:
                    click.echo(
                        f"FAILED: Unable to delete the profile {self.name}")
        else:
            click.echo(f"FAILED: The profile {self.name} doesn't exist")
