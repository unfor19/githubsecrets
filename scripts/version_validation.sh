#!/bin/bash
set -e

### README
### ---------------------------------------------------------------------------
### Usage:  $ bash version_validation.sh 1.0.2rc1
### Inputs:
###    RELEASE_VERSION: The version to validate
###                     Command line argument: Just like in the example above
###                     OR
###                     Environment variable: $ export RELEASE_VERSION=1.0.2rc1
###            VERBOSE: Prints ">> [LOG]" messages
###                     Environment variable: $ export VERBOSE=true
###       EXIT_ON_FAIL:
###                     Environment variable: $ export EXIT_ON_FAIL=true
### Output:
###               Good: Prints the version
###                     $ bash scripts/version_validation.sh 1.0.2rc1
###                     >> [LOG]: Passed - Release version is valid - 1.0.2rc1
###                     1.0.2rc1
###              Error: Raises an error (exit code = 1)
###                     $ bash scripts/version_validation.sh 1.0.2rc
###                     >> [ERROR]: Failed - Release version is invalid - 1.0.2rc
### ---------------------------------------------------------------------------


_RELEASE_VERSION=${RELEASE_VERSION:-$1}
_VERBOSE=${VERSION_VALIDATION_VERBOSE:-"true"}
_EXIT_ON_FAIL=${EXIT_ON_FAIL:-"true"}


msg_error(){
    local msg="$1"
    echo -e ">> [ERROR]: $msg"
    exit 1
}


msg_log(){
    local msg="$1"
    if [[ $_VERBOSE = "true" ]]; then
        echo -e ">> [LOG]: $msg"
    fi
}


if [[ $_RELEASE_VERSION =~ ^[0-9]+(\.[0-9]*)*(\.[0-9]+(a|b|rc)|(\.post)|(\.dev))*[0-9]+$ ]]; then
    msg_log "Passed - Release version is valid - $_RELEASE_VERSION"
    echo "$_RELEASE_VERSION"
else
    if [[ $_EXIT_ON_FAIL = "true" ]]; then
        msg_error "Failed - Release version is invalid - $_RELEASE_VERSION"
    else
        msg_log "Failed - Release version is invalid"
        echo ""
    fi
fi
