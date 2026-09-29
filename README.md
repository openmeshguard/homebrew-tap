# OpenMeshGuard Homebrew tap

Install the read-only Istio security posture scanner on macOS or Linux:

```sh
brew install openmeshguard/tap/openmeshguard
openmeshguard version
```

Supports Apple Silicon and Intel macOS, and arm64 and amd64 Linux. The formula
installs the prebuilt GitHub Release binary; a Go toolchain is not required.

Homebrew checks the archive's pinned SHA-256 before installation. It does not
verify Sigstore signatures during installation. Maintainers verify the signed
checksum file and all four signed archives against the exact release workflow
identity before generating a formula. This trusts the reviewed tap commit and
Homebrew's checksum enforcement. For independent publisher verification, follow
[the release verification instructions](https://github.com/openmeshguard/openmeshguard/blob/main/docs/releases/verification.md).
These are CLI binaries, with no Apple Developer ID signature or notarization
claim. Installation does not read Kubernetes configuration or contact a cluster.

## Update a published stable release

Requires Python 3, curl, and Cosign v3. Generate only after the upstream release
has finished verification and become public:

```sh
python3 scripts/update.py v0.1.0
brew audit --strict openmeshguard/tap/openmeshguard
brew install openmeshguard/tap/openmeshguard
brew test openmeshguard/tap/openmeshguard
```

The generator rejects drafts, prereleases, malformed tags, duplicate checksums,
and signature/checksum failures. It writes the formula only after all checks
succeed. Review the formula diff and merge it to publish an update; never replace
a published upstream archive or move its tag.

The manual update workflow pushes a review branch within this tap using its
repository-scoped GitHub token and records the comparison / pull-request creation
URL in the job summary. A maintainer opens and reviews the pull request, then
merges it to publish the formula. The workflow needs only contents-write access;
it does not create or approve pull requests. Run it with the exact newly published
stable tag (including future M7 releases). No cross-repository token is needed;
no formula is published while the upstream release is still a draft.

References: [Homebrew taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)
and [formula platform blocks](https://docs.brew.sh/Formula-Cookbook).
