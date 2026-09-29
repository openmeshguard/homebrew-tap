import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("update", Path(__file__).with_name("update.py"))
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


class GeneratorTests(unittest.TestCase):
    def test_four_pinned_targets(self):
        sums = {f"openmeshguard_0.1.0_{os}_{arch}.tar.gz": "a" * 64
                for os in ["darwin", "linux"] for arch in ["arm64", "amd64"]}
        formula = update.generate("v0.1.0", sums)
        self.assertEqual(formula.count('sha256 "'), 4)
        self.assertEqual(formula.count('      url "'), 4)
        self.assertIn('version=v0.1.0', formula)

    def test_reject_untrusted_tag_or_hash(self):
        for tag in ["v1.0.0-rc1", "v1.2.3\n", "../../main", "v1.2.3;id"]:
            with self.assertRaises(ValueError):
                update.generate(tag, {})
        with self.assertRaises(ValueError):
            update.generate("v0.1.0", {"openmeshguard_0.1.0_darwin_arm64.tar.gz": "invalid"})

    def test_publication_gate(self):
        for metadata in [
            '{"tag_name":"v0.1.0","draft":true,"prerelease":false}',
            '{"tag_name":"v0.1.0","draft":false,"prerelease":true}',
            '{"tag_name":"v0.2.0","draft":false,"prerelease":false}',
            '{}',
        ]:
            with patch.object(update.sys, 'argv', ['update.py', 'v0.1.0']), patch.object(update, 'run', return_value=metadata):
                with self.assertRaises(ValueError):
                    update.main()


if __name__ == "__main__":
    unittest.main()
