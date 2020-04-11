#!/bin/bash
PYTHON_VERSION=$(python -c 'import platform; print(platform.python_version())')
PYTHON_VERSION=$(echo $PYTHON_VERSION | sed "s|\.||g")
echo ">> INIT"
ghs init
echo ">> Add profile"
ghs profile-apply -p unfor19 -o unfor19 -t $GITHUB_TOKEN
echo ">> Add secret - TEST_${PYTHON_VERSION}"
ghs secret-apply  -p unfor19 -r githubsecrets -s "TEST_${PYTHON_VERSION}" -v oompaloompa
echo ">> List secrets"
ghs secret-list   -p unfor19 -r githubsecrets
echo ">> Get secret - TEST_${PYTHON_VERSION}"
ghs secret-get    -p unfor19 -r githubsecrets -s "TEST_${PYTHON_VERSION}"
echo ">> Delete secret - TEST_${PYTHON_VERSION}"
ghs secret-delete -p unfor19 -r githubsecrets -s "TEST_${PYTHON_VERSION}"
echo ">> Remove credentials file"
rm -r ~/.githubsecrets
