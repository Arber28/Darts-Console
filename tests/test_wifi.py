import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('wifi', Path(__file__).parents[1] / 'deploy/wifi-helper.py')
wifi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wifi)


class WifiTests(unittest.TestCase):
    def test_escaped_output(self):
        self.assertEqual(wifi.split_nmcli(r'*:Cafe\: A\\B:85:WPA2'), ['*', 'Cafe: A\\B', '85', 'WPA2'])

    def test_credentials_never_in_arguments(self):
        secret = 'secret!123'
        with tempfile.TemporaryDirectory() as directory, patch.object(wifi, 'PROFILES', Path(directory)), patch.object(wifi, 'checked', return_value='') as command:
            wifi.connect('Cafe; $(touch bad)', secret)
            self.assertNotIn(secret, repr(command.call_args_list))
            profile = next(Path(directory).iterdir()).read_text()
            self.assertIn('psk=' + secret, profile)
            self.assertIn('interface-name=wlp2s0', profile)

    def test_failure_removes_secret_file(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(wifi, 'PROFILES', Path(directory)), patch.object(wifi, 'checked', side_effect=RuntimeError('secret')), patch.object(wifi, 'run_nmcli'):
            with self.assertRaisesRegex(RuntimeError, 'fehlgeschlagen'):
                wifi.connect('Cafe', 'password123')
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_cannot_activate_lan_or_unknown_uuid(self):
        with patch.object(wifi, 'saved', return_value=[]), patch.object(wifi, 'checked') as command:
            with self.assertRaises(ValueError):
                wifi.activate('enp1s0')
            command.assert_not_called()

    def test_rejects_keyfile_injection(self):
        for ssid, password in [('bad\n[wifi]', 'password123'), ('ok', 'pw\nkey=x'), ('ok', 'short')]:
            with self.assertRaises(ValueError):
                wifi.connect(ssid, password)
