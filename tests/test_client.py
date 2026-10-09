import io
import json
import unittest
from unittest.mock import patch

from earthfireai_core.client import OllamaClient
from earthfireai_core.config import Settings


class Response:
    def __init__(self, payload): self.payload = payload
    def __enter__(self): return self
    def __exit__(self, *_): return False
    def read(self): return json.dumps(self.payload).encode()


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = OllamaClient(Settings(timeout=1))

    @patch("earthfireai_core.client.urlopen")
    def test_version_and_models(self, opener):
        opener.side_effect = [Response({"version": "0.test"}), Response({"models": [{"name": "demo:latest"}]})]
        self.assertEqual(self.client.version(), "0.test")
        self.assertEqual(self.client.models(), ["demo:latest"])

    @patch("earthfireai_core.client.urlopen")
    def test_chat(self, opener):
        opener.return_value = Response({"message": {"content": "达西定律"}})
        self.assertEqual(self.client.chat("解释"), "达西定律")
        request = opener.call_args.args[0]
        payload = json.loads(request.data)
        self.assertFalse(payload["stream"])

    def test_empty_prompt(self):
        with self.assertRaises(ValueError): self.client.chat("  ")


if __name__ == "__main__": unittest.main()
