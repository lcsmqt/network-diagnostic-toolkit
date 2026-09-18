"""Testes da CLI (subcomandos exercitados diretamente, sem subprocess)."""

from unittest.mock import patch

from src.cli import build_parser
from src.models import PingResult


def test_subnet_command_prints_json(capsys):
    parser = build_parser()
    args = parser.parse_args(["subnet", "192.168.1.0/24"])
    exit_code = args.func(args, {})
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "192.168.1.0" in captured.out


def test_ping_command_respects_allowlist(capsys):
    parser = build_parser()
    args = parser.parse_args(["ping", "127.0.0.1"])
    config = {"allowed_targets": ["127.0.0.1"]}
    fake_result = PingResult(target="127.0.0.1", reachable=True, latency_ms=1.0, method="tcp:80")

    with patch("src.cli.check_connectivity", return_value=fake_result):
        exit_code = args.func(args, config)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "127.0.0.1" in captured.out


def test_interfaces_command_returns_zero(capsys):
    parser = build_parser()
    args = parser.parse_args(["interfaces"])
    with patch("src.cli.list_interfaces", return_value=[]):
        exit_code = args.func(args, {})
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "[]"
