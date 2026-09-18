"""Coletor de resolucao DNS (nome -> enderecos IP)."""

from __future__ import annotations

import socket

from src.models import DnsResult


def resolve(hostname: str) -> DnsResult:
    """Resolve um hostname para uma lista ordenada de enderecos IP unicos."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        addresses = sorted({info[4][0] for info in infos})
        return DnsResult(hostname=hostname, addresses=addresses, resolved=True)
    except socket.gaierror as exc:
        return DnsResult(hostname=hostname, addresses=[], resolved=False, error=str(exc))
