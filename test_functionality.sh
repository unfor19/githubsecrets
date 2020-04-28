#!/bin/bash
error (){
    local msg=$1
    echo -e "\033[31mFATA[0000]\e[0m ${msg}"
    usage
    exit
}

usage()
{
  cat << EOF
usage: bash ./test_functionality.sh -p PROFILE_NAME -o GITHUB_OWNER -t TEST_GITHUB_TOKEN -r GITHUB_REPOSITORY
-p    | --PROFILE_NAME       (Required)    willy
-o    | --GITHUB_OWNER       (Required)    unfor19
-t    | --TEST_GITHUB_TOKEN  (Required)    empty
-r    | --GITHUB_REPOSITORY  (Required)    githubsecrets
-h    | --help                             Brings up this menu
EOF
}

PYTHON_VERSION=$(python -c 'import platform; print(platform.python_version())')
PYTHON_VERSION=$(echo $PYTHON_VERSION | sed "s|\.||g")
PROFILE_NAME=willy
GITHUB_OWNER=unfor19
GITHUB_REPOSITORY=githubsecrets
GITHUB_TOKEN=

while [ "$1" != "" ]; do
    case $1 in
        -p | --PROFILE_NAME )
            shift
            PROFILE_NAME=$1
        ;;   
        -o | --GITHUB_OWNER )
            shift
            GITHUB_OWNER=$1
        ;;       
        -t | --TEST_GITHUB_TOKEN )
            shift
            TEST_GITHUB_TOKEN=$1
        ;;             
        -r | --GITHUB_REPOSITORY )
            shift
            GITHUB_REPOSITORY=$1
        ;;                                        
        -h | --help ) usage
            exit
        ;;
        * )           usage
            exit 1
    esac
    shift
done

[[ -z $TEST_GITHUB_TOKEN ]] && error "GitHub Token is missing"

echo ">> INIT"
ghs --ci init
echo ">> List profiles - no profiles yet"
ghs --ci profile-list
echo ">> Add profile"
ghs --ci profile-apply -p $PROFILE_NAME -o $GITHUB_OWNER -t $TEST_GITHUB_TOKEN
echo ">> List profiles - Should see $PROFILE_NAME"
ghs --ci profile-list
echo ">> Add secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-apply  -p $PROFILE_NAME -r $GITHUB_REPOSITORY -s "TEST_${PYTHON_VERSION}" -v oompaloompa
echo ">> List secrets"
ghs --ci secret-list   -p $PROFILE_NAME -r $GITHUB_REPOSITORY
echo ">> Get secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-get    -p $PROFILE_NAME -r $GITHUB_REPOSITORY -s "TEST_${PYTHON_VERSION}"
echo ">> Delete secret - TEST_${PYTHON_VERSION}"
ghs --ci secret-delete -p $PROFILE_NAME -r $GITHUB_REPOSITORY -s "TEST_${PYTHON_VERSION}"
echo ">> Delete profile - $PROFILE_NAME"
ghs --ci profile-delete -p $PROFILE_NAME
