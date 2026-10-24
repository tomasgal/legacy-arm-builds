# Publishing the first binary release

No binary release is currently published. The planned package version is
`5.6.40+dfsg-0+deb8u12+local20261023.1`. See
[release-plan.json](release-plan.json) for the twelve selected filenames.

## Release prerequisites

1. Recover the original twelve deployed `.deb` files. Preserve their bytes.
   Other packages produced by the build have not received the same acceptance.
2. Recover the exact pre-build source tree, local changelog, and Debian packaging.
   Check its version, series, and the three patch hashes against this repository.
   Export the complete corresponding Debian source package, including `.dsc`,
   original upstream tarball, and local Debian packaging tarball. The base Debian
   source package alone is not the corresponding modified source.
3. Inspect binary control fields, local changelog additions, source metadata,
   build paths, and any proposed logs for private data or machine-specific
   configuration. Preserve required upstream attribution and licenses. Do not
   publish runtime/configuration backups, keys, credentials, or raw private logs.
4. Verify package metadata and generate binary checksums:

```sh
python3 php5/verify-debs.py /path/to/release-assets --write-checksums
```

The verifier checks package names, exact versions, architectures, and readable
payload archives. It does not assess private content, cryptographic publisher
authenticity, runtime safety, or the completeness of corresponding source.

5. Generate a final SHA256SUMS covering the exact release payload, including
   complete source and notices. Replace the plan's pending state only after
   import, inspection, and validation. Do not invent absent artifact hashes.
6. Create an immutable tag and GitHub Release for the inspected payload. Attach
   the twelve binaries, corresponding source package, SHA256SUMS, and applicable
   notices. A GitHub-generated archive of this recipe repository is not a
   replacement for the full corresponding source package.

Use GitHub Releases for binary assets. Preserve published assets rather than
silently replacing a file under an existing version. A rebuilt or changed payload
needs a distinct release identity. There is no automatic APT repository here.

## Installation guidance for readers

Evaluate these packages only on a matching Jessie armhf installation. Compare the
installed package inventory, dependencies, PHP API, SAPIs, and third-party
extensions. Keep all selected packages that require the exact php5-common version
consistent. Do not install every generated `.deb` indiscriminately.

Before modifying a deployment, retain the original exact-version packages and
configuration backups and prepare a recovery procedure. Validate CLI/extensions,
Apache configuration, service state, and application uploads. Ordinary uploads
and PHP session upload progress are different features; the latter is disabled
by patch 0261. Recovery must use that deployment's own original packages and
configuration, not another host's backup.

No download-and-install one-liner is provided while the release is incomplete.
