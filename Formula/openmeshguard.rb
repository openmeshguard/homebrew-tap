class Openmeshguard < Formula
  desc "Read-only Istio security posture scanner with evidence chains"
  homepage "https://github.com/openmeshguard/openmeshguard"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.1.0/openmeshguard_0.1.0_darwin_arm64.tar.gz"
      sha256 "30d7db7ecbae8495e5c54efdf3c2d3d2208fce8bd4d0d4e07d81f3be3a801f66"
    end
    on_intel do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.1.0/openmeshguard_0.1.0_darwin_amd64.tar.gz"
      sha256 "987d17f991330daa9427251ddca8fe79afd53d24785b5f3182b9099e48a9bbb2"
    end
  end
  on_linux do
    on_arm do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.1.0/openmeshguard_0.1.0_linux_arm64.tar.gz"
      sha256 "a18d7c275832def2dea7b00fe1d3cd38cb413da1b70cdff6966d6bec51688cbc"
    end
    on_intel do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.1.0/openmeshguard_0.1.0_linux_amd64.tar.gz"
      sha256 "0352a14d726e976f005f09c531b0c792d60b88165a308c6a6ad74f264fd3c8d2"
    end
  end

  def install
    bin.install "openmeshguard"
  end

  test do
    assert_match "version=v0.1.0", shell_output("#{bin}/openmeshguard version")
    assert_match "scan", shell_output("#{bin}/openmeshguard --help")
  end
end
