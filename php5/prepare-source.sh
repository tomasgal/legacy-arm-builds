#!/bin/sh
# SPDX-License-Identifier: MIT
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: sh php5/prepare-source.sh NEW_OUTPUT_DIRECTORY" >&2
    exit 2
fi
repo=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
for tool in curl tar sha256sum cmp dpkg-source dpkg-parsechangelog; do
    command -v "$tool" >/dev/null 2>&1 || { echo "Missing tool: $tool" >&2; exit 1; }
done
case "$1" in /*) work=$1;; *) work=$PWD/$1;; esac
if [ -e "$work" ] || [ -L "$work" ]; then
    echo "Output path already exists; choose a new directory: $work" >&2
    exit 1
fi
mkdir -p "$work"
base=5.6.40+dfsg-0+deb8u12
vendor=5.6.40-105+0~20261022.135+debian11~1.gbp37a17e
version=5.6.40+dfsg-0+deb8u12+local20261023.1+rebuild1
debian_url=https://archive.debian.org/debian-security/pool/updates/main/p/php5
vendor_url=https://packages.sury.org/php/pool/main/p/php5.6
cd "$work"
for f in php5_5.6.40+dfsg.orig.tar.gz "php5_${base}.debian.tar.xz" "php5_${base}.dsc"; do
    curl --fail --location --show-error --connect-timeout 15 --max-time 300 --output "$f" "$debian_url/$f"
done
vendor_archive=php5.6_${vendor}.debian.tar.xz
curl --fail --location --show-error --connect-timeout 15 --max-time 300 --output "$vendor_archive" "$vendor_url/$vendor_archive"
sha256sum -c "$repo/php5/inputs.sha256"
(cd "$repo/php5/patches" && sha256sum -c "$repo/php5/patches.sha256")
while IFS= read -r name; do
    [ -n "$name" ] || continue
    tar -xOf "$vendor_archive" "debian/patches/$name" | cmp - "$repo/php5/patches/$name"
done < "$repo/php5/patches/series"

# Recorded hashes are checked above; this deliberately does not authenticate
# the original DSC signature. See PROVENANCE.md before trusting these inputs.
dpkg-source --no-check -x "php5_${base}.dsc" php5-source
tree=$work/php5-source
while IFS= read -r name; do
    [ -n "$name" ] || continue
    if grep -Fqx "$name" "$tree/debian/patches/series"; then
        echo "Patch unexpectedly already in base series: $name" >&2
        exit 1
    fi
    cp "$repo/php5/patches/$name" "$tree/debian/patches/$name"
    printf '%s\n' "$name" >> "$tree/debian/patches/series"
done < "$repo/php5/patches/series"

# dpkg-source's quilt implementation applies unapplied series entries with
# zero fuzz and records them in .pc, preserving the original Debian patch state.
dpkg-source --before-build "$tree"
{
    printf 'php5 (%s) unstable; urgency=medium\n\n' "$version"
    printf '  * Reconstruct the Jessie runtime patch set using pinned vendor patches\n'
    printf '    0261, 0262 and 0263. This is a separately versioned recipe rebuild.\n\n'
    printf ' -- Legacy ARM Builds <builder@example.invalid>  %s\n\n' "$(LC_ALL=C date -R)"
    cat "$tree/debian/changelog"
} > "$tree/debian/changelog.new"
mv "$tree/debian/changelog.new" "$tree/debian/changelog"
actual=$(cd "$tree" && dpkg-parsechangelog | sed -n 's/^Version: //p')
test "$actual" = "$version"
printf 'SOURCE_PREPARED=%s\nPACKAGE_VERSION=%s\n' "$tree" "$version"
