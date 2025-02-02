from unittest import TestCase


class MyTests(TestCase):

    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        self.assertFalse(False)