class Openmeshguard < Formula
  desc "Read-only Istio security posture scanner with evidence chains"
  homepage "https://github.com/openmeshguard/openmeshguard"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.2.0/openmeshguard_0.2.0_darwin_arm64.tar.gz"
      sha256 "d199f837ce8657faddcfe3c61da2e3504183d7ee5c41c90f8f5a2628f3661870"
    end
    on_intel do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.2.0/openmeshguard_0.2.0_darwin_amd64.tar.gz"
      sha256 "3b113cbde2dbeb1de99de98da17db1eaf88e9c24c378d1ca6e4d384731ca5662"
    end
  end
  on_linux do
    on_arm do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.2.0/openmeshguard_0.2.0_linux_arm64.tar.gz"
      sha256 "48626d831d69523c8cea3e37c09f43faea106aa9ed6bb72aa4a631e60629a876"
    end
    on_intel do
      url "https://github.com/openmeshguard/openmeshguard/releases/download/v0.2.0/openmeshguard_0.2.0_linux_amd64.tar.gz"
      sha256 "420babc2002540cb12c950191d257e8fc3c7f4d37ef2f38e62ad1494eba3b028"
    end
  end

  def install
    bin.install "openmeshguard"
  end

  test do
    assert_match "version=v0.2.0", shell_output("#{bin}/openmeshguard version")
    assert_match "scan", shell_output("#{bin}/openmeshguard --help")
  end
end
