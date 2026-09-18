"""Calculadora de sub-redes (CIDR) usando a biblioteca padrao ``ipaddress``."""

from __future__ import annotations

import ipaddress

from src.models import SubnetInfo


def calculate_subnet(cidr: str) -> SubnetInfo:
    """Calcula rede, broadcast, mascara e faixa de hosts utilizaveis de um CIDR.

    Aceita tanto o endereco de rede quanto o endereco de um host dentro da
    rede (``strict=False``), o que e mais amigavel em uma CLI: o usuario nao
    precisa ja saber o endereco de rede "puro" para fazer a conta.
    """
    network = ipaddress.ip_network(cidr, strict=False)
    hosts = list(network.hosts())
    broadcast = str(network.broadcast_address) if network.version == 4 else None

    return SubnetInfo(
        cidr=str(network),
        network_address=str(network.network_address),
        broadcast_address=broadcast,
        netmask=str(network.netmask),
        total_addresses=network.num_addresses,
        usable_hosts=len(hosts),
        first_usable=str(hosts[0]) if hosts else None,
        last_usable=str(hosts[-1]) if hosts else None,
    )
