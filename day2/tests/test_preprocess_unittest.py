"""unittest 스타일 테스트 (2일차 1교시).

실행: day2 폴더에서  python -m pytest tests/test_preprocess_unittest.py
      또는          PYTHONPATH=src python -m unittest discover -s tests -p "test_*unittest.py"
"""

import unittest

import numpy as np
import pandas as pd

from mlqa.preprocess import impute_median, is_eligible


class TestIsEligible(unittest.TestCase):

    def test_typical_eligible(self):
        self.assertTrue(is_eligible(25, 12, False))

    def test_too_old(self):
        self.assertFalse(is_eligible(40, 12, False))

    def test_invalid_age_raises(self):
        with self.assertRaises(ValueError):
            is_eligible(200, 12, False)


class TestImputeMedian(unittest.TestCase):

    def setUp(self):
        self.train = pd.DataFrame({"x": [1.0, 2.0, np.nan, 4.0]})
        self.test = pd.DataFrame({"x": [np.nan, 100.0]})

    def test_no_missing_left(self):
        train_filled, test_filled, _ = impute_median(self.train, self.test, ["x"])
        self.assertEqual(train_filled["x"].isna().sum(), 0)
        self.assertEqual(test_filled["x"].isna().sum(), 0)

    def test_original_not_modified(self):
        impute_median(self.train, self.test, ["x"])
        self.assertTrue(self.train["x"].isna().any())


if __name__ == "__main__":
    unittest.main()
