#!/usr/bin/env python3
"""Generate a tap formula only after public release signature verification."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def run(*args):
    return subprocess.check_output(args, text=True)


def generate(tag, checksums):
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise ValueError("expected stable vMAJOR.MINOR.PATCH tag")
    version = tag[1:]
    blocks = []
    for os_name, brew_os in [("darwin", "macos"), ("linux", "linux")]:
        lines = [f"  on_{brew_os} do"]
        for arch, brew_arch in [("arm64", "arm"), ("amd64", "intel")]:
            name = f"openmeshguard_{version}_{os_name}_{arch}.tar.gz"
            sha = checksums[name]
            if not re.fullmatch(r"[a-f0-9]{64}", sha):
                raise ValueError("invalid checksum")
            lines += [f"    on_{brew_arch} do", f'      url "https://github.com/openmeshguard/openmeshguard/releases/download/{tag}/{name}"', f'      sha256 "{sha}"', "    end"]
        lines += ["  end"]
        blocks.append("\n".join(lines))
    return f'''class Openmeshguard < Formula
  desc "Read-only Istio security posture scanner with evidence chains"
  homepage "https://github.com/openmeshguard/openmeshguard"
  license "Apache-2.0"

{chr(10).join(blocks)}

  def install
    bin.install "openmeshguard"
  end

  test do
    assert_match "version=v{version}", shell_output("#{{bin}}/openmeshguard version")
    assert_match "scan", shell_output("#{{bin}}/openmeshguard --help")
  end
end
'''


def main():
    tag = sys.argv[1] if len(sys.argv) == 2 else ""
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise ValueError("usage: update.py vMAJOR.MINOR.PATCH")
    metadata = json.loads(run("curl", "-fsSL", f"https://api.github.com/repos/openmeshguard/openmeshguard/releases/tags/{tag}"))
    if metadata.get("tag_name") != tag or metadata.get("draft") is not False or metadata.get("prerelease") is not False:
        raise ValueError("only an already public stable release may update the tap")
    identity = f"https://github.com/openmeshguard/openmeshguard/.github/workflows/release.yml@refs/tags/{tag}"
    with tempfile.TemporaryDirectory() as work:
        directory = Path(work)
        def fetch(name):
            target = directory / name
            run("curl", "-fsSL", "--output", str(target), f"https://github.com/openmeshguard/openmeshguard/releases/download/{tag}/{name}")
            return target
        def verify(name):
            artifact = fetch(name)
            bundle = fetch(name + ".sigstore.json")
            run("cosign", "verify-blob", "--certificate-identity", identity, "--certificate-oidc-issuer", "https://token.actions.githubusercontent.com", "--bundle", str(bundle), str(artifact))
            return artifact
        sums = {}
        for line in verify("checksums.txt").read_text().splitlines():
            sha, name = line.split()
            if name in sums:
                raise ValueError("duplicate checksum")
            sums[name] = sha
        for os_name in ["darwin", "linux"]:
            for arch in ["amd64", "arm64"]:
                name = f"openmeshguard_{tag[1:]}_{os_name}_{arch}.tar.gz"
                artifact = verify(name)
                if hashlib.sha256(artifact.read_bytes()).hexdigest() != sums.get(name):
                    raise ValueError("archive checksum mismatch")
        formula = generate(tag, sums)
    destination = Path(__file__).resolve().parents[1] / "Formula/openmeshguard.rb"
    destination.write_text(formula)


if __name__ == "__main__":
    main()
