import unittest
from pathlib import Path
from stats_toolkit import (
    mean, median, mode, variance, std_dev, quartiles, 
    iqr_outliers, load_column, StatisticsAnalyzer
)


class TestCentralTendency(unittest.TestCase):
    
    def test_mean_of_known_values(self):
        self.assertAlmostEqual(mean([10.0, 20.0, 30.0]), 20.0)
        self.assertAlmostEqual(mean([1.5, 2.5, 3.5, 4.5]), 3.0)

    def test_median_even_and_odd_lengths(self):
        self.assertEqual(median([3.0, 1.0, 2.0]), 2.0)
        self.assertEqual(median([1.0, 4.0, 2.0, 3.0]), 2.5)

    def test_mode_with_ties(self):
        self.assertEqual(mode([1.0, 1.0, 2.0, 2.0, 3.0]), [1.0, 2.0])
        self.assertEqual(mode([5.0, 5.0, 5.0, 10.0]), [5.0])
        # Every value appears once -> returns empty list per project rules
        self.assertEqual(mode([10.0, 20.0, 30.0]), [])

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median([])
        with self.assertRaises(ValueError):
            mode([])


class TestSpread(unittest.TestCase):
    
    def test_sample_vs_population_variance(self):
        data = [10.0, 20.0, 30.0]
        self.assertAlmostEqual(variance(data, sample=True), 100.0)
        self.assertAlmostEqual(variance(data, sample=False), 66.66666667)

    def test_std_dev_single_value(self):
        with self.assertRaises(ValueError):
            std_dev([5.0], sample=True)


class TestOutliers(unittest.TestCase):
    
    def test_no_outliers_in_uniform_data(self):
        data = [10.0, 11.0, 12.0, 13.0, 14.0]
        res = iqr_outliers(data)
        self.assertEqual(len(res["outliers"]), 0)

    def test_detects_obvious_outlier(self):
        data = [10.0, 12.0, 11.0, 14.0, 13.0, 500.0]
        res = iqr_outliers(data)
        self.assertIn(500.0, res["outliers"])


class TestLoading(unittest.TestCase):
    
    def test_invalid_and_missing_values_are_rejected(self):
        dummy_path = Path("test_dummy_deposits.csv")
        
        with open(dummy_path, "w", encoding="utf-8") as f:
            f.write("town,daily_deposits_kes\n")
            f.write("Nairobi,100.0\n")
            f.write("Thika,abc\n")
            f.write("Machakos,\n")
            f.write("Nakuru,200.0\n")
            f.write("Nairobi,-\n")
            
        valid, skipped = load_column(dummy_path, "daily_deposits_kes")
    
        if dummy_path.exists():
            dummy_path.unlink()
            
        # Assertions
        self.assertEqual(valid, [100.0, 200.0])
        self.assertEqual(len(skipped), 3)  # 'abc', missing field, and '-' placeholder
        
        # Verify the raw text value of the first skipped row is captured correctly
        self.assertEqual(skipped[0][1], "abc")

if __name__ == "__main__":
    unittest.main()

