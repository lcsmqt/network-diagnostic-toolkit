"""Verificacao de portas TCP, restrita a alvos autorizados (allowlist)."""

from __future__ import annotations

import socket
import time

from src.models import PortCheckResult
from src.security import ensure_target_allowed


def check_port(
    target: str,
    port: int,
    allowed_targets: list[str],
    timeout: float = 1.5,
) -> PortCheckResult:
    """Verifica se uma unica porta TCP esta aberta em um alvo autorizado."""
    ensure_target_allowed(target, allowed_targets)

    start = time.perf_counter()
    try:
        with socket.create_connection((target, port), timeout=timeout):
            elapsed_ms = (time.perf_counter() - start) * 1000
        return PortCheckResult(target=target, port=port, open=True, latency_ms=round(elapsed_ms, 2))
    except (TimeoutError, ConnectionRefusedError):
        return PortCheckResult(target=target, port=port, open=False, latency_ms=None)
    except OSError as exc:
        return PortCheckResult(target=target, port=port, open=False, latency_ms=None, error=str(exc))


def scan_ports(
    target: str,
    ports: list[int],
    allowed_targets: list[str],
    timeout: float = 1.5,
) -> list[PortCheckResult]:
    """Verifica uma lista de portas TCP no mesmo alvo autorizado."""
    return [check_port(target, port, allowed_targets, timeout=timeout) for port in ports]
