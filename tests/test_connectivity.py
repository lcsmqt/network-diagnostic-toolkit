"""Testes do teste de conectividade TCP (com mocks; nenhuma rede real)."""

from unittest.mock import MagicMock, patch

import pytest

from src.collectors.connectivity import check_connectivity
from src.security import TargetNotAllowedError


def _fake_connection():
    context = MagicMock()
    context.__enter__.return_value = MagicMock()
    context.__exit__.return_value = False
    return context


def test_check_connectivity_reachable():
    with patch("socket.create_connection", return_value=_fake_connection()):
        result = check_connectivity("127.0.0.1", ["127.0.0.1"], port=80)
    assert result.reachable is True
    assert result.latency_ms is not None
    assert result.error is None


def test_check_connectivity_unreachable_reports_error():
    with patch("socket.create_connection", side_effect=ConnectionRefusedError("recusado")):
        result = check_connectivity("127.0.0.1", ["127.0.0.1"], port=9999)
    assert result.reachable is False
    assert result.latency_ms is None
    assert result.error is not None


def test_check_connectivity_blocks_target_outside_allowlist():
    with pytest.raises(TargetNotAllowedError):
        check_connectivity("8.8.8.8", ["127.0.0.1"])
