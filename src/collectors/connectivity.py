"""Teste de conectividade defensivo, restrito a alvos autorizados (allowlist)."""

from __future__ import annotations

import socket
import time

from src.models import PingResult
from src.security import ensure_target_allowed


def check_connectivity(
    target: str,
    allowed_targets: list[str],
    port: int = 80,
    timeout: float = 2.0,
) -> PingResult:
    """Mede alcancabilidade e latencia abrindo/fechando uma conexao TCP.

    Nao usamos ICMP (o "ping" tradicional) porque isso exige um socket raw e,
    na maioria dos sistemas, privilegios administrativos. Uma conexao TCP e
    uma aproximacao defensiva, portavel e sem privilegios especiais para medir
    se um alvo autorizado esta respondendo e com que latencia.
    """
    ensure_target_allowed(target, allowed_targets)

    start = time.perf_counter()
    try:
        with socket.create_connection((target, port), timeout=timeout):
            elapsed_ms = (time.perf_counter() - start) * 1000
        return PingResult(
            target=target, reachable=True, latency_ms=round(elapsed_ms, 2), method=f"tcp:{port}"
        )
    except OSError as exc:
        return PingResult(
            target=target, reachable=False, latency_ms=None, method=f"tcp:{port}", error=str(exc)
        )
