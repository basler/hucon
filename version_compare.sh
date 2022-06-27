#!/bin/bash
# version_compare.sh - compares numerical versions and versions with ascii remainders
#
# Copyright (C) 2019 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the CreativeCommons BY-SA 4.0. license.
# See the https://creativecommons.org/licenses/by-sa/4.0/ file for details.

#-----------------
# this base snippet is by https://stackoverflow.com/users/60075/craig-mcqueen
# at fetched from https://stackoverflow.com/a/31258615
# for compression purposes the debug stuff was removed

ascii_frag() {
    expr match "$1" "\([^[:digit:]]*\)"
}

ascii_remainder() {
    expr match "$1" "[^[:digit:]]*\(.*\)"
}

numeric_frag() {
    expr match "$1" "\([[:digit:]]*\)"
}

numeric_remainder() {
    expr match "$1" "[[:digit:]]*\(.*\)"
}

vercomp_debug() {
    OUT="$1"
    #echo "${OUT}"
}

# return 1 for $1 > $2
# return 2 for $1 < $2
# return 0 for equal
vercomp() {
    local WORK1="$1"
    local WORK2="$2"
    local NUM1="", NUM2="", ASCII1="", ASCII2=""

    while true; do
        vercomp_debug "ASCII compare"
        ASCII1=`ascii_frag "${WORK1}"`
        ASCII2=`ascii_frag "${WORK2}"`
        WORK1=`ascii_remainder "${WORK1}"`
        WORK2=`ascii_remainder "${WORK2}"`

        if [ "${ASCII1}" \> "${ASCII2}" ]; then
            return 1
        elif [ "${ASCII1}" \< "${ASCII2}" ]; then
            return 2
        fi

        NUM1=`numeric_frag "${WORK1}"`
        NUM2=`numeric_frag "${WORK2}"`
        WORK1=`numeric_remainder "${WORK1}"`
        WORK2=`numeric_remainder "${WORK2}"`

        if [ -z "${NUM1}" -a -z "${NUM2}" ]; then
            return 0
        elif [ -z "${NUM1}" -a -n "${NUM2}" ]; then
            return 2
        elif [ -n "${NUM1}" -a -z "${NUM2}" ]; then
            return 1
        fi

        if [ "${NUM1}" -gt "${NUM2}" ]; then
            return 1
        elif [ "${NUM1}" -lt "${NUM2}" ]; then
            return 2
        fi
    done
}
# base snippet end
#------------------
compare_versions()
{
  local INPUT_ONE="", INPUT_ONE_VERSION="", INPUT_ONE_SUFFIX=""
  local INPUT_TWO="", INPUT_TWO_VERSION="", INPUT_TWO_SUFFIX=""
  local VERSION_COMPARE=0

  local STABLE_EQ=0
  local STABLE_ONE=1
  local STABLE_TWO=2

  local UNSTABLE_EQ=3
  local UNSTABLE_ONE=4
  local UNSTABLE_TWO=5

  INPUT_ONE="$1"
  INPUT_TWO="$2"


  INPUT_ONE_VERSION=$(echo "${INPUT_ONE}" | cut -d'-' -f1)
  if [[ "${INPUT_ONE}" =~ "-" ]]; then
    INPUT_ONE_SUFFIX=$(echo "${INPUT_ONE}" | cut -d'-' -f2)
  fi

  INPUT_TWO_VERSION=$(echo "${INPUT_TWO}" | cut -d'-' -f1)
  if [[ "${INPUT_TWO}" =~ "-" ]]; then
    INPUT_TWO_SUFFIX=$(echo "${INPUT_TWO}" | cut -d'-' -f2)
  fi

  vercomp "${INPUT_ONE_VERSION}" "${INPUT_TWO_VERSION}"

  VERSION_COMPARE=$?

  if [ "${VERSION_COMPARE}" = "0" ]; then
      if [ -z "${INPUT_ONE_SUFFIX}" ] && [ -z "${INPUT_TWO_SUFFIX}" ]; then
        return ${STABLE_EQ};
      elif [ -z "${INPUT_ONE_SUFFIX}" ] && [ -n "${INPUT_TWO_SUFFIX}" ]; then
        return ${STABLE_ONE};
      elif [ -n "${INPUT_ONE_SUFFIX}" ] && [ -z "${INPUT_TWO_SUFFIX}" ]; then
        return ${STABLE_TWO};
      elif [ "${INPUT_ONE_SUFFIX}" = "${INPUT_TWO_SUFFIX}" ]; then
        return ${UNSTABLE_EQ};
      else
        vercomp "${INPUT_ONE_SUFFIX}" "${INPUT_TWO_SUFFIX}"
        return $((UNSTABLE_EQ+$?))
      fi
  elif [ "${VERSION_COMPARE}" = "1" ]; then
      if  [ -z "${INPUT_ONE_SUFFIX}" ]; then
        return ${STABLE_ONE};
      else
        return ${UNSTABLE_ONE}
      fi
  elif [ "${VERSION_COMPARE}" = "2" ]; then
      if  [ -z "${INPUT_TWO_SUFFIX}" ]; then
        return ${STABLE_TWO};
      else
        return ${UNSTABLE_TWO}
      fi
  fi
}

compare_versions $1 $2

echo $?
