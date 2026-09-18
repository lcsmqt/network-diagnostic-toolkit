"""Testes do coletor de interfaces (com mocks de psutil; portavel entre SOs)."""

from unittest.mock import MagicMock, patch

from src.collectors.interfaces import list_interfaces


class _FakeFamily:
    def __init__(self, name):
        self.name = name


def test_list_interfaces_parses_ipv4_ipv6_and_mac():
    fake_addrs = {
        "eth0": [
            MagicMock(family=_FakeFamily("AF_INET"), address="192.168.1.10"),
            MagicMock(family=_FakeFamily("AF_INET6"), address="fe80::1%eth0"),
            MagicMock(family=_FakeFamily("AF_LINK"), address="aa:bb:cc:dd:ee:ff"),
        ]
    }
    fake_stats = {"eth0": MagicMock(isup=True)}

    with patch("psutil.net_if_addrs", return_value=fake_addrs), \
         patch("psutil.net_if_stats", return_value=fake_stats):
        interfaces = list_interfaces()

    assert len(interfaces) == 1
    iface = interfaces[0]
    assert iface.name == "eth0"
    assert iface.ipv4 == ["192.168.1.10"]
    assert iface.ipv6 == ["fe80::1"]
    assert iface.mac == "aa:bb:cc:dd:ee:ff"
    assert iface.is_up is True


def test_list_interfaces_defaults_to_up_when_stats_missing():
    fake_addrs = {"lo": [MagicMock(family=_FakeFamily("AF_INET"), address="127.0.0.1")]}
    with patch("psutil.net_if_addrs", return_value=fake_addrs), \
         patch("psutil.net_if_stats", return_value={}):
        interfaces = list_interfaces()
    assert interfaces[0].is_up is True
