from os import getcwd, path
from setuptools import setup

# Change accordingly ----------------------------
PACKAGE_DIR_NAME = "githubsecrets"
GITHUB_OWNER = "unfor19"
GITHUB_REPOSITORY = "githubsecrets"
# -----------------------------------------------


# Keep the same structure, should NOT be changed
with open("version", "r") as fh:
    version = fh.read()

with open(path.join(getcwd(), 'src', PACKAGE_DIR_NAME, '__init__.py'), "w") as fh:  # noqa: E501
    fh.write(f"__version__ = '{version}'\n")

setup(
    version=version,
    download_url=f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/archive/{version}.tar.gz',  # noqa: E501
)
# -----------------------------------------------
