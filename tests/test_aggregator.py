"""Testes do agregador (com todos os coletores mockados)."""

from unittest.mock import patch

from src.aggregator import build_report
from src.models import DnsResult, InterfaceInfo, PingResult, PortCheckResult


def test_build_report_combines_all_collectors():
    config = {
        "allowed_targets": ["127.0.0.1"],
        "dns_lookups": ["example.com"],
        "ping_targets": ["127.0.0.1"],
        "port_checks": [{"target": "127.0.0.1", "ports": [22]}],
    }

    with patch(
        "src.aggregator.list_interfaces",
        return_value=[InterfaceInfo(name="lo", ipv4=["127.0.0.1"])],
    ), patch(
        "src.aggregator.resolve",
        return_value=DnsResult(hostname="example.com", addresses=["93.184.216.34"], resolved=True),
    ), patch(
        "src.aggregator.check_connectivity",
        return_value=PingResult(target="127.0.0.1", reachable=True, latency_ms=1.0, method="tcp:80"),
    ), patch(
        "src.aggregator.scan_ports",
        return_value=[PortCheckResult(target="127.0.0.1", port=22, open=True, latency_ms=0.5)],
    ):
        report = build_report(config)

    assert report.interfaces[0].name == "lo"
    assert report.dns_results[0].hostname == "example.com"
    assert report.ping_results[0].reachable is True
    assert report.port_results[0].port == 22
