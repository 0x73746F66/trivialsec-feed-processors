from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
import pytest

from app import (
    extract_ip_address,
    compare_contents,
)


def test_extract_ip_address_valid_ipv4():
    assert extract_ip_address("192.168.1.1") == IPv4Address("192.168.1.1")


def test_extract_ip_address_valid_ipv4_cidr():
    assert extract_ip_address("10.0.0.0/24") == IPv4Network("10.0.0.0/24")


def test_extract_ip_address_valid_ipv6():
    assert extract_ip_address("2001:db8::1") == IPv6Address("2001:db8::1")


def test_extract_ip_address_valid_ipv6_cidr():
    assert extract_ip_address("fe80::/64") == IPv6Network("fe80::/64")


def test_extract_ip_address_comment():
    assert extract_ip_address("# This is a comment") is None


def test_extract_ip_address_empty_line():
    assert extract_ip_address("") is None


def test_extract_ip_address_invalid_format():
    assert extract_ip_address("invalid_ip") is None


def test_compare_contents_added_ip():
    old_content = "10.0.0.1\n"
    new_content = old_content + "10.0.0.2\n"
    for ip_address in compare_contents(old_content, new_content):
        assert ip_address == IPv4Address("10.0.0.2")


def test_compare_contents_no_change():
    content = "192.168.1.1\n"
    added_ips = list(compare_contents(content, content))
    assert len(added_ips) == 0


def test_compare_contents_removed_ip():
    old_content = "10.0.0.1\n10.0.0.2\n"
    new_content = "10.0.0.1"
    for ip_address in compare_contents(old_content, new_content):
        assert ip_address == new_content
