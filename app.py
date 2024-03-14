from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

import validators


def extract_ip_address(line: str) -> IPv4Address | IPv4Network | IPv6Address | IPv6Network | None:
    if line.startswith('#') or not line:
        return None
    if ip_address := line.strip():
        if validators.ip_address.ipv4(ip_address, cidr=False, strict=True) is True:
            return IPv4Address(ip_address)
        if validators.ip_address.ipv6(ip_address, cidr=False, strict=True) is True:
            return IPv6Address(ip_address)
        if validators.ip_address.ipv4(ip_address, cidr=True, strict=True) is True:
            return IPv4Network(ip_address)
        if validators.ip_address.ipv6(ip_address, cidr=True, strict=True) is True:
            return IPv6Network(ip_address)
    return None

def compare_contents(old_contents: str, new_contents: str):
    old_index = set()
    for line in old_contents.splitlines():
        if ip_address := extract_ip_address(line):
            old_index.add(ip_address)

    for line in new_contents.splitlines():
        ip_address = extract_ip_address(line)
        if ip_address and ip_address not in old_index:
            yield ip_address
