import unittest
from routes import calculate_grade


class TestGradeCalculation(unittest.TestCase):
    """Test cases for grade calculation"""

    def test_grade_5_boundary(self):
        """Test grade 5 at boundary (90)"""
        self.assertEqual(calculate_grade(90), '5')

    def test_grade_5_above_boundary(self):
        """Test grade 5 above boundary"""
        self.assertEqual(calculate_grade(95), '5')
        self.assertEqual(calculate_grade(100), '5')

    def test_grade_4_boundary(self):
        """Test grade 4 at boundary (75)"""
        self.assertEqual(calculate_grade(75), '4')

    def test_grade_4_in_range(self):
        """Test grade 4 in valid range"""
        self.assertEqual(calculate_grade(80), '4')
        self.assertEqual(calculate_grade(89), '4')

    def test_grade_3_boundary(self):
        """Test grade 3 at boundary (50)"""
        self.assertEqual(calculate_grade(50), '3')

    def test_grade_3_in_range(self):
        """Test grade 3 in valid range"""
        self.assertEqual(calculate_grade(60), '3')
        self.assertEqual(calculate_grade(74), '3')

    def test_grade_2_boundary(self):
        """Test grade 2 at boundary (49)"""
        self.assertEqual(calculate_grade(49), '2')

    def test_grade_2_low_scores(self):
        """Test grade 2 for low scores"""
        self.assertEqual(calculate_grade(0), '2')
        self.assertEqual(calculate_grade(25), '2')

    def test_grade_none_score(self):
        """Test that None score returns None"""
        self.assertIsNone(calculate_grade(None))

    def test_grade_edge_cases(self):
        """Test edge cases between grades"""
        # Just below grade 5
        self.assertEqual(calculate_grade(89.9), '4')
        # Just below grade 4
        self.assertEqual(calculate_grade(74.9), '3')
        # Just below grade 3
        self.assertEqual(calculate_grade(49.9), '2')

    def test_grade_perfect_score(self):
        """Test perfect score"""
        self.assertEqual(calculate_grade(100), '5')

    def test_grade_zero_score(self):
        """Test zero score"""
        self.assertEqual(calculate_grade(0), '2')


if __name__ == '__main__':
    unittest.main()
