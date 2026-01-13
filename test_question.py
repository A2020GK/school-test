import unittest
from question import generate_question_advanced, check_answer


class TestQuestionGeneration(unittest.TestCase):
    """Test cases for question generation"""

    def test_generate_sqrt_question(self):
        """Test generating a square root question"""
        question, updated_asked, question_type = generate_question_advanced('sqrt', [])
        self.assertIsNotNone(question)
        self.assertIsInstance(question, int)
        self.assertIn(question_type, ['base', 'result'])
        self.assertEqual(len(updated_asked), 1)

    def test_generate_powers_question(self):
        """Test generating a powers of 2 question"""
        question, updated_asked, question_type = generate_question_advanced('powers', [])
        self.assertIsNotNone(question)
        self.assertIsInstance(question, int)
        self.assertIn(question_type, ['base', 'result'])
        self.assertEqual(len(updated_asked), 1)

    def test_sqrt_question_range(self):
        """Test that sqrt questions are in valid range (10-30)"""
        for _ in range(10):
            question, updated_asked, question_type = generate_question_advanced('sqrt', [])
            if question_type == 'base':
                self.assertGreaterEqual(question, 10)
                self.assertLessEqual(question, 30)

    def test_powers_question_range(self):
        """Test that powers questions are in valid range (0-14)"""
        for _ in range(10):
            question, updated_asked, question_type = generate_question_advanced('powers', [])
            if question_type == 'base':
                self.assertGreaterEqual(question, 0)
                self.assertLessEqual(question, 14)

    def test_no_duplicate_questions(self):
        """Test that the same question is not generated twice"""
        asked_questions = []
        question1, asked_questions, qtype1 = generate_question_advanced('sqrt', asked_questions)
        
        # Generate another question - should be different
        question2, asked_questions, qtype2 = generate_question_advanced('sqrt', asked_questions)
        
        # Should have 2 different questions tracked
        self.assertEqual(len(asked_questions), 2)
        self.assertNotEqual((question1, qtype1), (question2, qtype2))

    def test_invalid_mode(self):
        """Test that invalid mode raises ValueError"""
        with self.assertRaises(ValueError):
            generate_question_advanced('invalid', [])

    def test_all_questions_asked_sqrt(self):
        """Test behavior when all sqrt questions are asked"""
        # Create a list of all possible combinations for sqrt
        all_questions = [(base, qtype) for base in range(10, 31) 
                         for qtype in ['find_result', 'find_base']]
        
        with self.assertRaises(ValueError):
            generate_question_advanced('sqrt', all_questions)

    def test_all_questions_asked_powers(self):
        """Test behavior when all powers questions are asked"""
        # Create a list of all possible combinations for powers
        all_questions = [(base, qtype) for base in range(0, 15) 
                         for qtype in ['find_result', 'find_base']]
        
        with self.assertRaises(ValueError):
            generate_question_advanced('powers', all_questions)


class TestAnswerChecking(unittest.TestCase):
    """Test cases for answer checking"""

    def test_check_sqrt_base_correct(self):
        """Test checking correct answer for sqrt (given base, find result)"""
        result = check_answer('sqrt', 10, 'base', 100)
        self.assertTrue(result)

    def test_check_sqrt_base_incorrect(self):
        """Test checking incorrect answer for sqrt (given base, find result)"""
        result = check_answer('sqrt', 10, 'base', 99)
        self.assertFalse(result)

    def test_check_sqrt_result_correct(self):
        """Test checking correct answer for sqrt (given result, find base)"""
        result = check_answer('sqrt', 100, 'result', 10)
        self.assertTrue(result)

    def test_check_sqrt_result_incorrect(self):
        """Test checking incorrect answer for sqrt (given result, find base)"""
        result = check_answer('sqrt', 100, 'result', 11)
        self.assertFalse(result)

    def test_check_powers_base_correct(self):
        """Test checking correct answer for powers (given base, find result)"""
        result = check_answer('powers', 5, 'base', 32)
        self.assertTrue(result)

    def test_check_powers_base_incorrect(self):
        """Test checking incorrect answer for powers (given base, find result)"""
        result = check_answer('powers', 5, 'base', 31)
        self.assertFalse(result)

    def test_check_powers_result_correct(self):
        """Test checking correct answer for powers (given result, find base)"""
        result = check_answer('powers', 32, 'result', 5)
        self.assertTrue(result)

    def test_check_powers_result_incorrect(self):
        """Test checking incorrect answer for powers (given result, find base)"""
        result = check_answer('powers', 32, 'result', 6)
        self.assertFalse(result)

    def test_check_edge_case_sqrt_small_numbers(self):
        """Test sqrt with smallest valid base"""
        result = check_answer('sqrt', 10, 'base', 100)
        self.assertTrue(result)

    def test_check_edge_case_sqrt_large_numbers(self):
        """Test sqrt with largest valid base"""
        result = check_answer('sqrt', 30, 'base', 900)
        self.assertTrue(result)

    def test_check_edge_case_powers_zero(self):
        """Test powers with base 0"""
        result = check_answer('powers', 0, 'base', 1)
        self.assertTrue(result)

    def test_check_edge_case_powers_large(self):
        """Test powers with large base"""
        result = check_answer('powers', 10, 'base', 1024)
        self.assertTrue(result)

    def test_check_invalid_mode(self):
        """Test that invalid mode raises ValueError"""
        with self.assertRaises(ValueError):
            check_answer('invalid', 10, 'base', 100)

    def test_check_invalid_question_type(self):
        """Test that invalid question type raises ValueError"""
        with self.assertRaises(ValueError):
            check_answer('sqrt', 10, 'invalid', 100)

    def test_check_sqrt_non_perfect_square(self):
        """Test sqrt with non-perfect square should return False"""
        result = check_answer('sqrt', 50, 'result', 7)
        self.assertFalse(result)

    def test_check_powers_non_power_of_two(self):
        """Test powers with non-power of 2 should return False"""
        result = check_answer('powers', 33, 'result', 5)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
