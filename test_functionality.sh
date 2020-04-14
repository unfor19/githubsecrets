#!/bin/bash
PYTHON_VERSION=$(python -c 'import platform; print(platform.python_version())')
PYTHON_VERSION=$(echo $PYTHON_VERSION | sed "s|\.||g")
PROFILE_NAME=unfor19
REPOSITORY_NAME=githubsecrets

echo ">> INIT"
ghs --ci init
echo ">> List profiles - no profiles yet"
ghs --ci profile-list
echo ">> Add profile"
ghs --ci profile-apply -p $PROFILE_NAME -o $PROFILE_NAME -t $GITHUB_TOKEN
echo ">> List profiles - Should see $PROFILE_NAME"
ghs --ci profile-list
echo ">> Add secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-apply  -p $PROFILE_NAME -r $REPOSITORY_NAME -s "TEST_${PYTHON_VERSION}" -v oompaloompa
echo ">> List secrets"
ghs --ci secret-list   -p $PROFILE_NAME -r $REPOSITORY_NAME
echo ">> Get secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-get    -p $PROFILE_NAME -r $REPOSITORY_NAME -s "TEST_${PYTHON_VERSION}"
echo ">> Delete secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-delete -p $PROFILE_NAME -r $REPOSITORY_NAME -s "TEST_${PYTHON_VERSION}"
echo ">> Delete profile - $PROFILE_NAME"
ghs --ci profile-delete -p $PROFILE_NAME
echo ">> Remove credentials file"
rm -r ~/.githubsecrets
