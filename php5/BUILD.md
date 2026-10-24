# Source preparation and native armhf build

## What has and has not been reproduced

The deployed binaries were built natively in a separate Debian Jessie armhf
chroot, using GCC 4.9.2, an unprivileged build account, fakeroot, and the original
Debian package rules. The build used `parallel=1 nocheck` and was not an upstream
or full Debian test-suite run.

The helper in this repository is a new, sanitized reconstruction of the source
preparation procedure. It fetches hash-pinned inputs, checks the vendored patches
against the vendor archive, and applies the same runtime patch set. It creates
the separate revision `5.6.40+dfsg-0+deb8u12+local20261023.1+rebuild1` and a generic
changelog identity. These metadata are not claimed to match the deployed build.

The original chroot bootstrap and its archive-signature handling are not yet
published. This repository does not provide a validated, unattended chroot
bootstrap. Use an independently prepared and appropriately authenticated Jessie
armhf build environment. Do not solve expired archive metadata by disabling
package authentication globally or changing a production clock.

## Original released source

For the original revision, download all three corresponding source files and `SHA256SUMS` from the [release](https://github.com/tomasgal/legacy-arm-builds/releases/tag/php5-jessie-armhf-local20261023.1). Verify the checksums, then extract the local descriptor:

```sh
grep -E '[.]dsc$|[.]orig[.]tar[.]gz$|[.]debian[.]tar[.]xz$' SHA256SUMS | sha256sum -c -
dpkg-source --no-check -x php5_5.6.40+dfsg-0+deb8u12+local20261023.1.dsc
```

The descriptor is unsigned; the checksum check is not independent publisher authentication. Build that extracted source in a matching, independently prepared Jessie armhf environment using the native command below. No bit-for-bit output claim is made.

## Prepare separate recipe source

Requires Linux/POSIX shell, curl, tar with xz/gzip support, sha256sum, cmp,
dpkg-source, and dpkg-parsechangelog. Run as an ordinary user. The output path
must not exist; it contains downloads and the resulting source tree.

```sh
sh php5/prepare-source.sh "$HOME/builds/php5-jessie-rebuild1"
```

The `.dsc` signature is explicitly not verified by this helper. See the
[provenance boundary](PROVENANCE.md#integrity-boundary).

## Build inside the prepared Jessie armhf environment

Install the source package's declared build dependencies inside that environment.
Keep dependency installation and service-start suppression confined to the build
environment. As the unprivileged build user, from the prepared source directory:

```sh
dpkg-checkbuilddeps && DEB_BUILD_OPTIONS="parallel=1 nocheck" dpkg-buildpackage -b -us -uc -rfakeroot
```

This performs no production installation. The packaging builds several SAPIs and
extensions; it can produce more packages than the selected twelve. Building an
extension or SAPI does not establish that its request handling was tested.

## Corresponding source and reproducibility

For any binaries that will be redistributed, retain the exact prepared source,
local changelog, patch series, packaging, declared build dependencies, and tool
versions. Export a complete Debian source package from a clean copy of that
source. Preserve component licenses and inspect local metadata before release.

A new build from this recipe is a different build. Do not replace an already
published release asset or relabel it as the original deployed binary. No
bit-for-bit reproducibility claim is made.
