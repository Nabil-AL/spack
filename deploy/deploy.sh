#!/bin/bash -l

# This script assumes that the following variables are set in the environment:
#
# DEPLOYMENT_ROOT: path to deploy to

# Make sure that no modules interfere with the build
module purge all

set -o errexit
set -o nounset

DEFAULT_DEPLOYMENT_ROOT="/gpfs/bbp.cscs.ch/ssd/apps/hpc/test/$(whoami)/deployment"
DEFAULT_DEPLOYMENT_DATA="/gpfs/bbp.cscs.ch/ssd/apps/hpc/download"
DEFAULT_DEPLOYMENT_DATE="$(date +%Y-%m-%d)"

# Set variables to default. The user may override the following:
#
# * `DEPLOYMENT_ROOT` for the installation directory
# * `DEPLOYMENT_DATA` containing tarballs of proprietary software
# * `DEPLOYMENT_DATE` to force a date for the installation directory
#
# for the latter, see also the comment of `last_install_dir`
DEPLOYMENT_DATA=${DEPLOYMENT_DATA:-${DEFAULT_DEPLOYMENT_DATA}}
DEPLOYMENT_ROOT=${DEPLOYMENT_ROOT:-${DEFAULT_DEPLOYMENT_ROOT}}

SPACK_SOURCE_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/sources"
SPACK_BINARY_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/binaries"
SPACK_PROPRIETARY_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/proprietary"

export DEPLOYMENT_ROOT SPACK_BINARY_MIRROR_DIR SPACK_SOURCE_MIRROR_DIR SPACK_PROPRIETARY_MIRROR_DIR

PATH=/usr/bin:${PATH}

export PATH

. ./deploy.lib

usage() {
    echo "usage: $0 [-cgil] stage..." 1>&2
    exit 1
}

do_copy_config=default
do_copy_modules=default
do_generate=default
do_install=default
while getopts "cgilm" arg; do
    case "${arg}" in
        c)
            do_copy_config=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_copy_modules} = "default" ]] && do_copy_modules=no
            ;;
        g)
            do_generate=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_copy_config} = "default" ]] && do_copy_config=no
            [[ ${do_copy_modules} = "default" ]] && do_copy_modules=no
            ;;
        i)
            do_install=yes
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_copy_config} = "default" ]] && do_copy_config=no
            [[ ${do_copy_modules} = "default" ]] && do_copy_modules=no
            ;;
        l)
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_copy_config} = "default" ]] && do_copy_config=no
            [[ ${do_copy_modules} = "default" ]] && do_copy_modules=no
            ;;
        m)
            do_copy_modules=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_copy_config} = "default" ]] && do_copy_config=no
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND - 1))

declare -A stage_map
for what in ${stages}; do
    stage_map[${what}]=1
done

if [[ "$@" = "all" ]]; then
    set -- ${stages}
else
    unknown=
    for what in "$@"; do
        if [[ ! ${stage_map[${what}]+_} ]]; then
            unknown="${unknown} ${what}"
        fi
    done
    if [[ -n "${unknown}" ]]; then
        echo "unknown stage(s):${unknown}"
        echo "allowed:          ${stages}"
        exit 1
    fi
fi

declare -A desired
for what in "$@"; do
    desired[${what}]=Yes
done

unset $(set +x; env | awk -F= '/^(PMI|SLURM)_/ {print $1}' | xargs)

[[ ${do_generate} = "yes" ]] && generate_specs "$@"

for what in ${stages}; do
    if [[ ${desired[${what}]+_} ]]; then
        if [[ ${do_install} != "no" ]]; then
            install_specs ${what}
        fi
        if [[ ${do_copy_config} = "yes" ]]; then
            copy_user_configuration ${what}
        fi
        if [[ ${do_copy_modules} = "yes" ]]; then
            copy_modules ${what}
        fi
    fi
done
