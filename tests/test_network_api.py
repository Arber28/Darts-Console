import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location('api', Path(__file__).parents[1] / 'deploy/api-server.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class ApiTests(unittest.TestCase):
    def handler(self, path, headers, body=b'{}'):
        handler = object.__new__(api.Handler)
        handler.path = path
        handler.headers = headers
        handler.rfile = io.BytesIO(body)
        handler.json_reply = Mock()
        handler.network_helper = Mock()
        return handler

    def test_foreign_origin_cannot_connect(self):
        h = self.handler('/api/network/connect', {'Host': '127.0.0.1:8765', 'Origin': 'https://evil.test', 'X-Darts-Network': 'requested'})
        h.do_POST()
        self.assertEqual(h.json_reply.call_args.args[0], 403)
        h.network_helper.assert_not_called()

    def test_scan_requires_custom_header(self):
        h = self.handler('/api/network/scan', {'Host': '127.0.0.1:8765'})
        h.do_GET()
        self.assertEqual(h.json_reply.call_args.args[0], 403)
        h.network_helper.assert_not_called()

    def test_oversized_credentials_rejected_before_read(self):
        h = self.handler('/api/network/connect', {'Host': 'localhost:8765', 'Origin': 'http://localhost:8765', 'X-Darts-Network': 'requested', 'Content-Type': 'application/json', 'Content-Length': '9000'})
        h.do_POST()
        self.assertEqual(h.json_reply.call_args.args[0], 413)
        h.network_helper.assert_not_called()
