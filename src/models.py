"""Estruturas de dados do toolkit de diagnostico de rede."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InterfaceInfo:
    """Interface de rede local com seus enderecos."""

    name: str
    ipv4: list[str] = field(default_factory=list)
    ipv6: list[str] = field(default_factory=list)
    mac: str | None = None
    is_up: bool = True


@dataclass
class DnsResult:
    """Resultado de uma resolucao DNS."""

    hostname: str
    addresses: list[str]
    resolved: bool
    error: str | None = None


@dataclass
class PingResult:
    """Resultado de um teste de conectividade (TCP connect)."""

    target: str
    reachable: bool
    latency_ms: float | None
    method: str
    error: str | None = None


@dataclass
class PortCheckResult:
    """Resultado da verificacao de uma porta TCP em um alvo."""

    target: str
    port: int
    open: bool
    latency_ms: float | None
    error: str | None = None


@dataclass
class SubnetInfo:
    """Informacoes calculadas de uma sub-rede CIDR."""

    cidr: str
    network_address: str
    broadcast_address: str | None
    netmask: str
    total_addresses: int
    usable_hosts: int
    first_usable: str | None
    last_usable: str | None


@dataclass
class NetworkReport:
    """Snapshot completo do diagnostico de rede, pronto para exportacao."""

    generated_at: str
    interfaces: list[InterfaceInfo]
    dns_results: list[DnsResult]
    ping_results: list[PingResult]
    port_results: list[PortCheckResult]
