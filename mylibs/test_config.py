import os
import sys
import unittest
from unittest.mock import patch
import importlib

import mylibs
from mylibs.config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        """Runs before every single test. Clears config out of memory."""
        
        if 'mylibs.config' in sys.modules:
            del sys.modules['mylibs.config']

    @patch.dict(os.environ, {"GEMINI_API_KEY": "mock_gemini_key_12345"})
    def test_config_loads_successfully_when_env_exists(self):
        """Test that Config successfully initializes when keys are present."""
        # Dynamically import config after mocking os.environ
        from mylibs.config import Config
        
        self.assertEqual(Config.GEMINI_API_KEY, "mock_gemini_key_12345")
        #self.assertEqual(Config.ENVIRONMENT, "development") # checks fallback default

    @patch.dict(os.environ, {}) # Force environment to be completely empty
    def test_config_raises_value_error_when_key_missing(self):
        """Test that Config.validate() raises ValueError if GEMINI_API_KEY is missing."""
        # Ensure GEMINI_API_KEY is definitely stripped from testing environment
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
            
        # This will raise KeyError if the key is missing, which is expected
        # Expecting a ValueError to be thrown the moment 'config' is imported
        with self.assertRaises(ValueError) as context:
            from mylibs.config import Config  # Importing Config will trigger validation
            Config.validate()  # Explicitly call validate to ensure it raises the error
        self.assertIn("Missing critical environment secrets", str(context.exception))

if __name__ == "__main__":
    unittest.main()