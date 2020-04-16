import click
from .config import pass_config, pass_validate, create_artifacts
from .profile import Profile
from .secret import Secret


@click.group()
@pass_config
@click.option('--ci', is_flag=True, help="Use this flag to avoid deletion confirmation prompts")  # noqa: E501
def cli(config, ci):
    """All commands can run without providing options, and then you'll be prompted to insert values.\n
Secrets' values and Personal-Access-Tokens are hidden when prompted"""  # noqa: E501
    config.ci = ci  # noqa: F821


@cli.command()
@pass_config
def init(config):
    """Create a credentials file to store your profiles"""
    create_artifacts(config)


@cli.command()
@pass_validate
@pass_config
@click.option('--profile-name', '-p', prompt=True)
@click.option('--github-owner', '-o', prompt=True)
@click.option(
    '--personal-access-token', '-t', prompt=True,
    hide_input=True, confirmation_prompt=True
)
def profile_apply(
    config, validate,
    profile_name, github_owner, personal_access_token
):
    """Create or modify a profile"""
    profile = Profile(config, profile_name)
    profile.apply(github_owner, personal_access_token)


@cli.command()
@pass_validate
@pass_config
@click.option('--profile-name', '-p', prompt=True)
def profile_delete(
    config, validate,
    profile_name
):
    """Delete a profile"""
    profile = Profile(config, profile_name)
    profile.delete()


@cli.command()
@pass_validate
@pass_config
def profile_list(config, validate):
    """List all profile - truncates personal access tokens"""
    Profile.lista()


@cli.command()
@pass_validate
@pass_config
@click.option('--repository', '-r', prompt=True)
@click.option('--profile-name', '-p', prompt=True)
@click.option('--secret-name', '-s', prompt=True)
@click.option(
    '--secret-value', '-v', prompt=True,
    hide_input=True, confirmation_prompt=True
)
def secret_apply(
    config, validate,
    repository, profile_name, secret_name, secret_value
):
    """Create or modify a secret in a GitHub repository"""
    profile = Profile(config, profile_name)
    secret = Secret(config, profile, repository, secret_name, secret_value)
    secret.apply()


@cli.command()
@pass_validate
@pass_config
@click.option('--repository', '-r', prompt=True)
@click.option('--profile-name', '-p', prompt=True)
@click.option('--secret-name', '-s', prompt=True)
def secret_delete(
    config, validate,
    repository, profile_name, secret_name
):
    """Delete a secret in a GitHub repository"""
    profile = Profile(config, profile_name)
    secret = Secret(config, profile, repository, secret_name)
    secret.delete()


@cli.command()
@pass_validate
@pass_config
@click.option('--repository', '-r', prompt=True)
@click.option('--profile-name', '-p', prompt=True)
@click.option('--secret-name', '-s', prompt=True)
def secret_get(
    config, validate,
    repository, profile_name, secret_name
):
    """Get a secret from a GitHub repository"""
    profile = Profile(config, profile_name)
    secret = Secret(config, profile, repository, secret_name)
    secret.get()


@cli.command()
@pass_validate
@pass_config
@click.option('--repository', '-r', prompt=True)
@click.option('--profile-name', '-p', prompt=True)
def secret_list(
    config, validate,
    repository, profile_name
):
    """List all secret in a GitHub repository"""
    profile = Profile(config, profile_name)
    secret = Secret(config, profile, repository)
    secret.lista()
