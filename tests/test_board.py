import unittest

from detection.board import consensus, segment


class BoardTest(unittest.TestCase):
    def test_board_regions(self):
        for point, hit in [
            ((0, 0), (25, 2)), ((0, -12), (25, 1)), ((0, -103), (20, 3)),
            ((165, 0), (6, 2)), ((0, 35), (3, 1)), ((-75, 0), (11, 1)),
            ((0, -172), (0, 0)),
        ]:
            self.assertEqual(segment(*point), hit)

    def test_agreement_and_ambiguity(self):
        self.assertEqual(consensus([[(0, -103)], [(2, -104)], [(0, 60)]]),
                         {"n": 20, "m": 3, "views": 2})
        self.assertIsNone(consensus([[(0, -103), (0, 60)], [(0, 60), (2, -104)], []]))
        self.assertIsNone(consensus([[(0, -103)], [], []]))
