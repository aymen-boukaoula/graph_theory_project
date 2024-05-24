import unittest
from gui import GraphApp

class TestGUI(unittest.TestCase):
    def test_app_creation(self):
        app = GraphApp()
        self.assertIsNotNone(app)

if __name__ == '__main__':
    unittest.main()
