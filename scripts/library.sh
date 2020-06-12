#!/usr/bin/env bash

#
# Commands
#

FIND="${FIND:-find}"
GIT="${GIT:-git}"
GSUTIL="${GSUTIL:-gsutil}"
PYTHON="${PYTHON:-python}"
SED="${SED:-sed}"
SHA256SUM="${SHA256SUM:-shasum -a 256}"

#
#
#

relay::sdk::python::sha256sum() {
  $SHA256SUM | cut -d' ' -f1
}

relay::sdk::python::escape_shell() {
  printf '%s\n' "'${*//\'/\'\"\'\"\'}'"
}

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

relay::sdk::python::release_vars() {
  RELEASE_VERSION="$( relay::sdk::python::release_version || true )"
  if [ -z "${RELEASE_VERSION}" ]; then
    printf 'RELEASE_VERSION=\n'
    return
  fi

  # Parse the version information.
  IFS='.' read RELEASE_VERSION_MAJOR RELEASE_VERSION_MINOR RELEASE_VERSION_PATCH <<<"${RELEASE_VERSION}"

  printf 'RELEASE_VERSION=%s\n' "$( relay::sdk::python::escape_shell "${RELEASE_VERSION}" )"
  printf 'RELEASE_VERSION_MAJOR=%s\n' "$( relay::sdk::python::escape_shell "${RELEASE_VERSION_MAJOR}" )"
  printf 'RELEASE_VERSION_MINOR=%s\n' "$( relay::sdk::python::escape_shell "${RELEASE_VERSION_MINOR}" )"
  printf 'RELEASE_VERSION_PATCH=%s\n' "$( relay::sdk::python::escape_shell "${RELEASE_VERSION_PATCH}" )"
}

relay::sdk::python::release() {
  if [[ "$#" -ne 4 ]]; then
    echo "usage: ${FUNCNAME[0]} <bucket> <filename> <dist-prefix> <dist-ext>" >&2
    return 1
  fi

  relay::sdk::python::release_check
  eval "$( relay::sdk::python::release_vars )"

  local KEY_PREFIX FILENAME DIST_PREFIX DIST_EXT
  KEY_PREFIX="gs://$1/sdk/python"
  FILENAME="$2"
  DIST_PREFIX="$3"
  DIST_EXT="$4"

  (
    set -x

    local KEY KEY_MAJOR_MINOR KEY_MAJOR
    KEY="${KEY_PREFIX}/v${RELEASE_VERSION}/${DIST_PREFIX}${RELEASE_VERSION}${DIST_EXT}"
    KEY_MAJOR_MINOR="${KEY_PREFIX}/v${RELEASE_VERSION_MAJOR}.${RELEASE_VERSION_MINOR}/${DIST_PREFIX}${RELEASE_VERSION_MAJOR}.${RELEASE_VERSION_MINOR}${DIST_EXT}"
    KEY_MAJOR="${KEY_PREFIX}/v${RELEASE_VERSION_MAJOR}/${DIST_PREFIX}${RELEASE_VERSION_MAJOR}${DIST_EXT}"

    $GSUTIL cp "${FILENAME}" "${KEY}"
    $GSUTIL cp "${KEY}" "${KEY_MAJOR_MINOR}"
    $GSUTIL cp "${KEY}" "${KEY_MAJOR}"
  )
}

# If we're in a CI context, we may need to force the version.
if [ -n "${GIT_TAG_OVERRIDE:-}" ]; then
  export SETUPTOOLS_SCM_PRETEND_VERSION="${GIT_TAG_OVERRIDE##v}"
fi
