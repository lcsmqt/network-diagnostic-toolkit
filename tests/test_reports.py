"""Testes dos renderizadores de relatorio (JSON e Markdown)."""

import json

from src.models import DnsResult, InterfaceInfo, NetworkReport, PingResult, PortCheckResult
from src.reports.json_report import render_json
from src.reports.markdown_report import render_markdown


def _sample_report() -> NetworkReport:
    return NetworkReport(
        generated_at="2026-01-01T00:00:00+00:00",
        interfaces=[InterfaceInfo(name="eth0", ipv4=["192.168.1.10"], is_up=True)],
        dns_results=[DnsResult(hostname="example.com", addresses=["93.184.216.34"], resolved=True)],
        ping_results=[PingResult(target="127.0.0.1", reachable=True, latency_ms=1.23, method="tcp:80")],
        port_results=[PortCheckResult(target="127.0.0.1", port=22, open=True, latency_ms=0.98)],
    )


def test_render_json_round_trips_through_json_loads():
    payload = json.loads(render_json(_sample_report()))
    assert payload["interfaces"][0]["name"] == "eth0"
    assert payload["dns_results"][0]["resolved"] is True


def test_render_markdown_contains_expected_sections():
    markdown = render_markdown(_sample_report())
    assert "# Relatorio de Diagnostico de Rede" in markdown
    assert "## Interfaces" in markdown
    assert "eth0" in markdown
    assert "example.com" in markdown
