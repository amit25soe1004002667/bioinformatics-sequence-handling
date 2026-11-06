import unittest

from sequence_stats import summarize_sequence


class SequenceStatsTests(unittest.TestCase):
    def test_balanced_sequence(self):
        result = summarize_sequence("ATGCGCATTA")
        self.assertEqual(result["length"], 10)
        self.assertEqual(result["gc_percent"], 40.0)
        self.assertEqual((result["A"], result["C"], result["G"], result["T"]), (3, 2, 2, 3))
        self.assertEqual(result["other"], 0)

    def test_ambiguous_bases_are_reported(self):
        result = summarize_sequence("ATGCNNNN")
        self.assertEqual(result["length"], 8)
        self.assertEqual(result["gc_percent"], 25.0)
        self.assertEqual(result["other"], 4)

    def test_empty_sequence(self):
        result = summarize_sequence("")
        self.assertEqual(result["length"], 0)
        self.assertEqual(result["gc_percent"], 0.0)


if __name__ == "__main__":
    unittest.main()