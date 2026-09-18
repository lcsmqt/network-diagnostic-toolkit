"""Interface de linha de comando do toolkit de diagnostico de rede."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.aggregator import build_report
from src.collectors.connectivity import check_connectivity
from src.collectors.dns import resolve
from src.collectors.interfaces import list_interfaces
from src.collectors.ports import scan_ports
from src.config import load_config
from src.logging_setup import configure_logging
from src.reports.json_report import render_json
from src.reports.markdown_report import render_markdown
from src.subnet import calculate_subnet


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_interfaces(args: argparse.Namespace, config: dict[str, Any]) -> int:
    interfaces = list_interfaces()
    _print_json([asdict(item) for item in interfaces])
    return 0


def cmd_dns(args: argparse.Namespace, config: dict[str, Any]) -> int:
    result = resolve(args.hostname)
    _print_json(asdict(result))
    return 0 if result.resolved else 1


def cmd_ping(args: argparse.Namespace, config: dict[str, Any]) -> int:
    result = check_connectivity(args.target, config["allowed_targets"], port=args.port)
    _print_json(asdict(result))
    return 0 if result.reachable else 1


def cmd_port_check(args: argparse.Namespace, config: dict[str, Any]) -> int:
    ports = [int(item) for item in args.ports.split(",")]
    results = scan_ports(args.target, ports, config["allowed_targets"])
    _print_json([asdict(item) for item in results])
    return 0


def cmd_subnet(args: argparse.Namespace, config: dict[str, Any]) -> int:
    info = calculate_subnet(args.cidr)
    _print_json(asdict(info))
    return 0


def cmd_report(args: argparse.Namespace, config: dict[str, Any]) -> int:
    report = build_report(config)
    content = render_json(report) if args.format == "json" else render_markdown(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Relatorio gravado em {output_path}")
    else:
        print(content)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Toolkit de diagnostico de rede (defensivo, restrito a alvos autorizados)."
    )
    parser.add_argument("--config", help="Caminho do YAML de configuracao (padrao: config/config.yaml)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "interfaces", help="Lista interfaces de rede locais"
    ).set_defaults(func=cmd_interfaces)

    dns_parser = subparsers.add_parser("dns", help="Resolve um hostname")
    dns_parser.add_argument("hostname")
    dns_parser.set_defaults(func=cmd_dns)

    ping_parser = subparsers.add_parser(
        "ping", help="Testa conectividade TCP com um alvo autorizado (allowlist)"
    )
    ping_parser.add_argument("target")
    ping_parser.add_argument("--port", type=int, default=80)
    ping_parser.set_defaults(func=cmd_ping)

    port_parser = subparsers.add_parser(
        "port-check", help="Verifica portas TCP em um alvo autorizado (allowlist)"
    )
    port_parser.add_argument("target")
    port_parser.add_argument("--ports", default="22,80,443", help="Portas separadas por virgula")
    port_parser.set_defaults(func=cmd_port_check)

    subnet_parser = subparsers.add_parser("subnet", help="Calcula informacoes de uma sub-rede CIDR")
    subnet_parser.add_argument("cidr")
    subnet_parser.set_defaults(func=cmd_subnet)

    report_parser = subparsers.add_parser("report", help="Gera relatorio de inventario de rede")
    report_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    report_parser.add_argument("--output", help="Caminho do arquivo de saida (opcional)")
    report_parser.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args.config)
    configure_logging(config["log_level"])

    try:
        return args.func(args, config)
    except Exception as exc:  # noqa: BLE001 - erro amigavel na CLI, detalhes no log
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
