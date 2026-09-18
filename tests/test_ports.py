"""Testes da verificacao de portas TCP (com mocks; nenhuma rede real)."""

from unittest.mock import MagicMock, patch

import pytest

from src.collectors.ports import check_port, scan_ports
from src.security import TargetNotAllowedError


def _fake_connection():
    context = MagicMock()
    context.__enter__.return_value = MagicMock()
    context.__exit__.return_value = False
    return context


def test_check_port_open():
    with patch("socket.create_connection", return_value=_fake_connection()):
        result = check_port("127.0.0.1", 22, ["127.0.0.1"])
    assert result.open is True
    assert result.latency_ms is not None


def test_check_port_closed_is_not_an_error():
    with patch("socket.create_connection", side_effect=ConnectionRefusedError()):
        result = check_port("127.0.0.1", 9999, ["127.0.0.1"])
    assert result.open is False
    assert result.error is None


def test_scan_ports_checks_every_port_and_blocks_unallowed_targets():
    with patch("socket.create_connection", return_value=_fake_connection()):
        results = scan_ports("127.0.0.1", [22, 80, 443], ["127.0.0.1"])
    assert [item.port for item in results] == [22, 80, 443]
    assert all(item.open for item in results)

    with pytest.raises(TargetNotAllowedError):
        scan_ports("8.8.8.8", [80], ["127.0.0.1"])
