"""Testes da calculadora de sub-redes."""

from src.subnet import calculate_subnet


def test_calculate_subnet_slash_24():
    info = calculate_subnet("192.168.1.0/24")
    assert info.network_address == "192.168.1.0"
    assert info.broadcast_address == "192.168.1.255"
    assert info.netmask == "255.255.255.0"
    assert info.total_addresses == 256
    assert info.usable_hosts == 254
    assert info.first_usable == "192.168.1.1"
    assert info.last_usable == "192.168.1.254"


def test_calculate_subnet_accepts_host_address_not_just_network_address():
    info = calculate_subnet("10.0.0.5/28")
    assert info.network_address == "10.0.0.0"
    assert info.cidr == "10.0.0.0/28"


def test_calculate_subnet_slash_31_point_to_point():
    info = calculate_subnet("10.0.0.0/31")
    assert info.total_addresses == 2
    assert info.usable_hosts == 2


def test_calculate_subnet_slash_32_single_host():
    info = calculate_subnet("10.0.0.5/32")
    assert info.total_addresses == 1
    assert info.usable_hosts == 1
    assert info.first_usable == "10.0.0.5"
