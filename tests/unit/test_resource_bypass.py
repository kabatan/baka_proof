from __future__ import annotations

import unittest

from scripts.check_resource_bypass import main


class ResourceBypassTest(unittest.TestCase):
    def test_no_unapproved_popen_usage(self) -> None:
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
