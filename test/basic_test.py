from unittest import IsolatedAsyncioTestCase

from dropbox_notifier import DropboxNotifierApp


class BasicCache(IsolatedAsyncioTestCase):
    def test_simple(self):
        self.assertEqual(2 + 2, 4)

    def test_instantiate(self):
        app = DropboxNotifierApp()
        self.assertNotEqual(app, None)
