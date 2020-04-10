from setuptools import setup, find_packages

setup(
    name='githubsecrets',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pynacl',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        ghs=scripts.githubsecrets:cli
    ''',
)
