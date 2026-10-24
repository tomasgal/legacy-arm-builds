#!/bin/sh
# SPDX-License-Identifier: MIT
# CLI-only failure-path smoke: the specified PHP process is expected to exit.
set -eu
if [ "$#" -ne 1 ]; then
    echo 'Usage: sh php5/tests/oom-cli.sh /absolute/path/to/php5' >&2
    exit 2
fi
case "$1" in /*) php=$1;; *) echo 'Use an absolute PHP executable path' >&2; exit 2;; esac
test -x "$php"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' 0
export LEGACY_ARM_OOM_MARKER=$work/shutdown
if "$php" -n -d memory_limit=8M -d display_errors=1 -r 'register_shutdown_function("file_put_contents", getenv("LEGACY_ARM_OOM_MARKER"), "called"); str_repeat("x",33554432);' > "$work/output" 2>&1; then
    echo OOM_TEST_UNEXPECTED_SUCCESS >&2
    exit 1
else
    rc=$?
fi
cat "$work/output"
test "$rc" -eq 1
grep -q 'Allowed memory size' "$work/output"
test ! -e "$work/shutdown"
echo OOM_SMOKE_OK
