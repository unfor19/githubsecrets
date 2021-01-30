import click
from .config import pass_config, pass_validate, create_artifacts, \
    list_by_comma, print_pretty_json, is_docker
from .profile import Profile
from .secret import Secret


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        aliases = {
            "p": "profile",
            "s": "secret",
            "a": "apply",
            "g": "get",
            "d": "delete",
            "l": "list",
        }
        if len(cmd_name) == 2:
            words = [aliases[char] for char in cmd_name if char in aliases]
            cmd_name = "-".join(words)

        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")


# @click.group()
@ click.command(cls=AliasedGroup)
@ pass_config
@ click.option('--ci', '-ci', is_flag=True, help="Use this flag to avoid deletion confirmation prompts")  # noqa: E501
def cli(config, ci):
    """All commands can run without providing options, and then you'll be prompted to insert values.\n
Secrets' values and Personal-Access-Tokens are hidden when prompted"""  # noqa: E501
    if is_docker():
        ci = True
    config.ci = ci  # noqa: F821


@ cli.command()
@ pass_config
def init(config):
    """Create a credentials file to store your profiles"""
    create_artifacts(config)


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--profile-name', '-p', prompt=True)
@ click.option('--github-owner', '-o', prompt=True)
@ click.option(
    '--personal-access-token', '-t', prompt=True,
    hide_input=True, confirmation_prompt=True


)
def profile_apply(
    config, validate,
    profile_name, github_owner, personal_access_token
):
    """[pa] Create or modify multiple profiles providing a string delimited by commas ","\n
Example: ghs profile-apply -p 'willy, oompa'"""  # noqa: 501
    profile_names = list_by_comma(profile_name)
    for prof_name in profile_names:
        profile = Profile(config, prof_name)
        profile.apply(github_owner, personal_access_token)


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--profile-name', '-p', prompt=True)
def profile_delete(
    config, validate,
    profile_name
):
    """[pd] Delete multiple profiles providing a string delimited by commas ","\n
Example: ghs profile-delete -p 'willy, oompa'"""
    profile_names = list_by_comma(profile_name)
    for prof_name in profile_names:
        profile = Profile(config, prof_name)
        profile.delete()


@ cli.command()
@ pass_validate
@ pass_config
def profile_list(config, validate):
    """[pl] List all profile - truncates personal access tokens"""
    Profile.lista()


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--repository', '-r', prompt=True)
@ click.option('--profile-name', '-p', prompt=True)
@ click.option('--secret-name', '-s', prompt=True)
@ click.option(
    '--secret-value', '-v', prompt=True,
    hide_input=True, confirmation_prompt=True
)
def secret_apply(
    config, validate,
    repository, profile_name, secret_name, secret_value
):
    """[sa] Apply to multiple repositories providing a string delimited by commas ","\n
Example: ghs secret-apply -p willy -r 'githubsecrets, serverless-template'"""  # noqa: 501
    profile = Profile(config, profile_name)
    repositories = list_by_comma(repository)
    responses = []
    for repo in repositories:
        secret = Secret(config, profile, repo, secret_name, secret_value)
        secret.apply()
        responses.append(secret.apply())
    print_pretty_json(responses)


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--repository', '-r', prompt=True)
@ click.option('--profile-name', '-p', prompt=True)
@ click.option('--secret-name', '-s', prompt=True)
def secret_delete(
    config, validate,
    repository, profile_name, secret_name
):
    """[sd] Delete secrets from multiple repositories providing a string delimited by commas ","\n
Example: ghs secret-delete -p willy -r 'githubsecrets, serverless-template'"""  # noqa: 501
    profile = Profile(config, profile_name)
    repositories = list_by_comma(repository)
    responses = []
    for repo in repositories:
        secret = Secret(config, profile, repo, secret_name)
        responses.append(secret.delete())
    print_pretty_json(responses)


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--repository', '-r', prompt=True)
@ click.option('--profile-name', '-p', prompt=True)
@ click.option('--secret-name', '-s', prompt=True)
def secret_get(
    config, validate,
    repository, profile_name, secret_name
):
    """[sg] Get secrets from multiple repositories providing a string delimited by commas ","\n
Example: ghs secret-get -p willy -r 'githubsecrets, serverless-template'"""  # noqa: 501
    profile = Profile(config, profile_name)
    repositories = list_by_comma(repository)
    responses = []
    for repo in repositories:
        secret = Secret(config, profile, repo, secret_name)
        responses.append(secret.get())
    print_pretty_json(responses)


@ cli.command()
@ pass_validate
@ pass_config
@ click.option('--repository', '-r', prompt=True)
@ click.option('--profile-name', '-p', prompt=True)
def secret_list(
    config, validate,
    repository, profile_name
):
    """[sl] List secrets of multiple repositories providing a string delimited by commas ","\n
Example: ghs secret-delete -p willy -r 'githubsecrets, serverless-template'"""  # noqa: 501
    profile = Profile(config, profile_name)
    repositories = list_by_comma(repository)
    responses = []
    for repo in repositories:
        secret = Secret(config, profile, repo)
        responses.append(secret.lista())
    print_pretty_json(responses)
