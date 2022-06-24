import unittest
from unittest.mock import MagicMock, patch

import reactivex as rx
from reactivex import operators as ops
from utils.ops import ops_ping


class TestOps(unittest.TestCase):
    @patch("utils.ping.ping_ip")
    def test_ops_ping_pingable_ips(self, mock_ping_ip: MagicMock) -> None:
        def ping_ip_side_effect(ip: str) -> str:
            return ip

        mock_ping_ip.side_effect = ping_ip_side_effect
        ip_tuple_list = [("192.168.1.1", "192.168.2.1"), ("192.168.1.2", "192.168.2.2")]
        obs = rx.from_(ip_tuple_list).pipe(
            ops_ping(),
            ops.filter(lambda ips: ips[0] or ips[1]),
        )
        res = []
        obs.subscribe(on_next=res.append)
        assert res == [("192.168.1.1", "192.168.2.1"), ("192.168.1.2", "192.168.2.2")]

    @patch("utils.ping.ping_ip")
    def test_ops_ping_non_pingable_ips(self, mock_ping_ip: MagicMock) -> None:
        def ping_ip_side_effect(ip: str) -> str:
            raise ConnectionError(f"{ip} is not active")

        mock_ping_ip.side_effect = ping_ip_side_effect
        ip_tuple_list = [("192.168.1.1", "192.168.2.1"), ("192.168.1.2", "192.168.2.2")]
        obs = rx.from_(ip_tuple_list).pipe(
            ops_ping(),
            ops.filter(lambda ips: ips[0] or ips[1]),
        )
        res = []
        obs.subscribe(on_next=res.append)
        assert res == []
