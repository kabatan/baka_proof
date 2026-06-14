from __future__ import annotations

import unittest

from scripts.check_geometry_full2d_facade import check_facade


class GeometryFull2DFacadeTest(unittest.TestCase):
    def test_facade_checker_passes(self) -> None:
        self.assertEqual(check_facade(), [])


if __name__ == "__main__":
    unittest.main()
