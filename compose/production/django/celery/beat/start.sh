#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A sct_annotation.taskapp beat -l INFO
