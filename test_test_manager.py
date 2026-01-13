import unittest
from test_manager import TestManager


class TestTestManager(unittest.TestCase):
    """Test cases for TestManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = TestManager()

    def test_initial_state(self):
        """Test initial state of TestManager"""
        self.assertFalse(self.manager.is_test_active())
        self.assertTrue(self.manager.is_finalized())
        self.assertIsNone(self.manager.get_current_variant())

    def test_start_test_powers(self):
        """Test starting a test with powers variant"""
        result = self.manager.start_test('powers')
        self.assertTrue(result)
        self.assertTrue(self.manager.is_test_active())
        self.assertFalse(self.manager.is_finalized())
        self.assertEqual(self.manager.get_current_variant(), 'powers')

    def test_start_test_squares(self):
        """Test starting a test with squares variant"""
        result = self.manager.start_test('squares')
        self.assertTrue(result)
        self.assertTrue(self.manager.is_test_active())
        self.assertFalse(self.manager.is_finalized())
        self.assertEqual(self.manager.get_current_variant(), 'squares')

    def test_start_test_invalid_variant(self):
        """Test starting a test with invalid variant"""
        result = self.manager.start_test('invalid')
        self.assertFalse(result)
        self.assertFalse(self.manager.is_test_active())
        self.assertTrue(self.manager.is_finalized())

    def test_start_test_when_not_finalized(self):
        """Test that you can't start a test when previous is not finalized"""
        self.manager.start_test('powers')
        self.manager.stop_test()
        # Now test is stopped but not finalized
        result = self.manager.start_test('squares')
        self.assertFalse(result)

    def test_stop_test(self):
        """Test stopping an active test"""
        self.manager.start_test('powers')
        result = self.manager.stop_test()
        self.assertTrue(result)
        self.assertFalse(self.manager.is_test_active())
        self.assertFalse(self.manager.is_finalized())

    def test_stop_test_when_not_active(self):
        """Test stopping a test that's not active"""
        result = self.manager.stop_test()
        self.assertFalse(result)

    def test_finalize_test(self):
        """Test finalizing a test"""
        self.manager.start_test('powers')
        self.manager.stop_test()
        self.manager.finalize_test()
        self.assertFalse(self.manager.is_test_active())
        self.assertTrue(self.manager.is_finalized())
        self.assertIsNone(self.manager.get_current_variant())

    def test_finalize_active_test(self):
        """Test finalizing an active test (should stop it)"""
        self.manager.start_test('powers')
        self.manager.finalize_test()
        self.assertFalse(self.manager.is_test_active())
        self.assertTrue(self.manager.is_finalized())
        self.assertIsNone(self.manager.get_current_variant())

    def test_full_test_lifecycle(self):
        """Test complete test lifecycle: start -> stop -> finalize -> start again"""
        # Start first test
        self.manager.start_test('powers')
        self.assertTrue(self.manager.is_test_active())
        
        # Stop test
        self.manager.stop_test()
        self.assertFalse(self.manager.is_test_active())
        
        # Finalize test
        self.manager.finalize_test()
        self.assertTrue(self.manager.is_finalized())
        
        # Start second test
        result = self.manager.start_test('squares')
        self.assertTrue(result)
        self.assertTrue(self.manager.is_test_active())
        self.assertEqual(self.manager.get_current_variant(), 'squares')

    def test_variant_persistence(self):
        """Test that variant persists until finalized"""
        self.manager.start_test('powers')
        self.manager.stop_test()
        # Variant should still be set even after stopping
        self.assertEqual(self.manager.get_current_variant(), 'powers')
        
        # After finalization, variant should be None
        self.manager.finalize_test()
        self.assertIsNone(self.manager.get_current_variant())


if __name__ == '__main__':
    unittest.main()
