from unittest import IsolatedAsyncioTestCase


class BasicCache(IsolatedAsyncioTestCase):
    def test_simple(self):
        self.assertEqual(2 + 2, 4)
