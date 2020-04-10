#!/bin/bash
source ./pack.sh
GHS_VERSION=$(cat ./version)
twine upload "dist/githubsecrets-${GHS_VERSION}.tar.gz" "dist/githubsecrets-${GHS_VERSION}-py3-none-any.whl"