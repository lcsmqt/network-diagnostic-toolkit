"""Agrega os coletores em um snapshot unico (``NetworkReport``)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.collectors.connectivity import check_connectivity
from src.collectors.dns import resolve
from src.collectors.interfaces import list_interfaces
from src.collectors.ports import scan_ports
from src.models import NetworkReport


def build_report(config: dict[str, Any]) -> NetworkReport:
    """Constroi um ``NetworkReport`` combinando todos os coletores.

    ``config`` segue o formato de ``config/config.example.yaml``:
    ``allowed_targets``, ``dns_lookups``, ``ping_targets`` e ``port_checks``
    (lista de ``{"target": ..., "ports": [...]}``).
    """
    allowed_targets: list[str] = config.get("allowed_targets", ["127.0.0.1", "localhost"])
    dns_targets: list[str] = config.get("dns_lookups", [])
    ping_targets: list[str] = config.get("ping_targets", allowed_targets)
    port_targets: list[dict[str, Any]] = config.get("port_checks", [])

    interfaces = list_interfaces()
    dns_results = [resolve(hostname) for hostname in dns_targets]
    ping_results = [check_connectivity(target, allowed_targets) for target in ping_targets]

    port_results = []
    for entry in port_targets:
        port_results.extend(
            scan_ports(entry["target"], entry.get("ports", []), allowed_targets)
        )

    return NetworkReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        interfaces=interfaces,
        dns_results=dns_results,
        ping_results=ping_results,
        port_results=port_results,
    )
