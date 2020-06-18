#!/usr/bin/env bash

#
# Commands
#

FIND="${FIND:-find}"
GIT="${GIT:-git}"
PYTHON="${PYTHON:-python}"
SED="${SED:-sed}"

#
#
#

relay::sdk::python::package_name() {
  $PYTHON setup.py --name
}

relay::sdk::python::package_name_wheel() {
  # See https://www.python.org/dev/peps/pep-0427/
  relay::sdk::python::package_name | $SED -Ee 's/[^A-Za-z0-9_.]+/_/g'
}

relay::sdk::python::package_artifacts() {
  if [[ "$#" -ne 1 ]]; then
    echo "usage: ${FUNCNAME[0]} <directory>" >&2
    return 1
  fi

  local PACKAGE_VERSION
  PACKAGE_VERSION="$( $PYTHON setup.py --version )"

  $FIND "$1" \
    -type f \
    -name "$( relay::sdk::python::package_name )-${PACKAGE_VERSION}"'*.tar.gz' \
    -or -name "$( relay::sdk::python::package_name_wheel )-${PACKAGE_VERSION}"'*.whl'
}

relay::sdk::python::git_tag() {
  printf "%s\n" "${GIT_TAG_OVERRIDE:-$( $GIT tag --points-at HEAD 'v*.*.*' )}"
}

relay::sdk::python::release_version() {
  local GIT_TAG GIT_CHANGED_FILES
  GIT_TAG="$( relay::sdk::python::git_tag )"
  GIT_CHANGED_FILES="$( $GIT status --short )"

  # Check for releasable version: if we have no tags or any changed files, we
  # can't release.
  if [ -z "${GIT_TAG}" ] || [ -n "${GIT_CHANGED_FILES}" ]; then
    return 1
  fi

  # Arbitrarily pick the first line.
  read GIT_TAG_A <<<"${GIT_TAG}"

  printf "%s\n" "${GIT_TAG_A#v}"
}

relay::sdk::python::release_check() {
  if ! relay::sdk::python::release_version >/dev/null; then
    echo "$0: no release tag (this commit must be tagged with the format vX.Y.Z)" >&2
    return 2
  fi
}

# If we're in a CI context, we may need to force the version.
if [ -n "${GIT_TAG_OVERRIDE:-}" ]; then
  export SETUPTOOLS_SCM_PRETEND_VERSION="${GIT_TAG_OVERRIDE##v}"
fi
