"""Coletor de interfaces de rede locais (nomes, IPs e status)."""

from __future__ import annotations

import psutil

from src.models import InterfaceInfo


def list_interfaces() -> list[InterfaceInfo]:
    """Lista as interfaces de rede locais com seus enderecos IPv4/IPv6/MAC.

    Usa ``psutil`` em vez de parsear ``/proc/net`` ou chamar ``ipconfig``/``ip``
    diretamente, o que mantem o coletor portavel entre Linux e Windows -- o
    mesmo raciocinio adotado no linux-system-health-toolkit.
    """
    addrs_by_interface = psutil.net_if_addrs()
    stats_by_interface = psutil.net_if_stats()

    interfaces: list[InterfaceInfo] = []
    for name, entries in addrs_by_interface.items():
        stats = stats_by_interface.get(name)
        info = InterfaceInfo(name=name, is_up=stats.isup if stats else True)

        for entry in entries:
            family_name = getattr(entry.family, "name", str(entry.family))
            if family_name == "AF_INET":
                info.ipv4.append(entry.address)
            elif family_name == "AF_INET6":
                # Remove o sufixo de scope-id (ex.: "%eth0") para ficar legivel.
                info.ipv6.append(entry.address.split("%")[0])
            elif family_name in ("AF_LINK", "AF_PACKET"):
                info.mac = entry.address or info.mac

        interfaces.append(info)

    return interfaces
