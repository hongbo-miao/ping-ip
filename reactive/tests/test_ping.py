import unittest
from unittest.mock import MagicMock, patch

from tenacity import RetryError
from utils.ping import ping_ip, ping_ips


class TestPing(unittest.TestCase):
    @patch("subprocess.call")
    def test_ping_ip_succeed(self, mock_subprocess_call: MagicMock) -> None:
        mock_subprocess_call.return_value = 0
        self.assertEqual(ping_ip("192.168.1.42"), "192.168.1.42")

    @patch("subprocess.call")
    def test_ping_ip_failed(self, mock_subprocess_call: MagicMock) -> None:
        with self.assertRaises(RetryError):
            mock_subprocess_call.return_value = 2
            self.assertEqual(ping_ip("192.168.1.42"), "192.168.1.42")

    @patch("utils.ping.ping_ip")
    def test_ping_ips(self, mock_ping_ip: MagicMock) -> None:
        def ping_ip_side_effect(ip: str) -> str:
            return ip

        mock_ping_ip.side_effect = ping_ip_side_effect
        self.assertEqual(
            ping_ips("192.168.1.42", "192.168.2.42"), ("192.168.1.42", "192.168.2.42")
        )
