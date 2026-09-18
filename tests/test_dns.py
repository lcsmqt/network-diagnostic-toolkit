"""Testes do coletor de DNS (com mocks; nenhuma consulta real de rede)."""

import socket
from unittest.mock import patch

from src.collectors.dns import resolve


def test_resolve_success():
    fake_infos = [(socket.AF_INET, 1, 6, "", ("93.184.216.34", 0))]
    with patch("socket.getaddrinfo", return_value=fake_infos):
        result = resolve("example.com")
    assert result.resolved is True
    assert result.addresses == ["93.184.216.34"]
    assert result.error is None


def test_resolve_deduplicates_and_sorts_addresses():
    fake_infos = [
        (socket.AF_INET, 1, 6, "", ("10.0.0.2", 0)),
        (socket.AF_INET, 1, 6, "", ("10.0.0.1", 0)),
        (socket.AF_INET, 1, 6, "", ("10.0.0.1", 0)),
    ]
    with patch("socket.getaddrinfo", return_value=fake_infos):
        result = resolve("dup.example.com")
    assert result.addresses == ["10.0.0.1", "10.0.0.2"]


def test_resolve_failure_returns_error_without_raising():
    with patch("socket.getaddrinfo", side_effect=socket.gaierror("nome nao encontrado")):
        result = resolve("invalido.invalido")
    assert result.resolved is False
    assert result.addresses == []
    assert result.error is not None
