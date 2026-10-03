"""Relatorio Markdown do diagnostico de rede."""

from __future__ import annotations

from src.models import NetworkReport


def render_markdown(report: NetworkReport) -> str:
    interfaces = "\n".join(f"- {item.name}" for item in report.interfaces) or "- nenhuma"
    dns = "\n".join(f"- {item.hostname}" for item in report.dns_results) or "- nenhum"
    return (
        "# Relatorio de Diagnostico de Rede\n\n"
        "## Interfaces\n\n"
        f"{interfaces}\n\n"
        "## DNS\n\n"
        f"{dns}\n"
    )
