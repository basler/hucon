""" HuConNetiface.py - Get information about network interfaces.

    Copyright (C) 2021 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""
import re
import subprocess
from typing import Callable, NamedTuple, Optional


class NetInterfaceInfo(NamedTuple):
    mac_address: Optional[str]
    ipv4_address: Optional[str]


SubprocessRunner = Callable[..., subprocess.CompletedProcess]

def get_info(
        interface_name: str,
        run_subprocess: SubprocessRunner = subprocess.run
    ) -> NetInterfaceInfo:
    """ Get info about network interface """
    result = _run_ip_addr_show(interface_name, run_subprocess=run_subprocess)
    info = _parse_ip_addr_show_output(result.stdout)
    return info


def _run_ip_addr_show(
        interface_name: str, run_subprocess: SubprocessRunner
    ) -> subprocess.CompletedProcess:
    """ Run command "ip addr show <interface_name>" as subprocess """
    return run_subprocess(
        ["ip", "addr", "show", interface_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        universal_newlines=True
    )


def _parse_ip_addr_show_output(output: str) -> NetInterfaceInfo:
    """
    Parse output of "ip addr show <interface>"
    """
    def find_mac(line: str) -> Optional[str]:
        mac_line_pattern = (
            "link.*? (?P<mac>{two_hex_digits}(:{two_hex_digits})*)"
            .format(
                two_hex_digits="[0-9a-fA-F]{2}"
            )
        )
        m = re.match(mac_line_pattern, line)
        if not m:
            return None
        return m.group("mac")

    def find_ipv4(line: str) -> Optional[str]:
        ipv4_line_pattern = (
            r"inet (?P<ipv4>{decimal_byte}(\.{decimal_byte}){{3}})"
            .format(
                decimal_byte="[0-9]{1,3}"
            )
        )
        m = re.match(ipv4_line_pattern, line)
        if not m:
            return None
        return m.group("ipv4")

    lines = [line.strip() for line in output.splitlines()]
    mac_addr = None
    ipv4_addr = None
    for line in lines:
        mac = find_mac(line)
        if mac is not None:
            mac_addr = mac

        ipv4 = find_ipv4(line)
        if ipv4 is not None:
            ipv4_addr = ipv4
    info = NetInterfaceInfo(mac_address=mac_addr, ipv4_address=ipv4_addr)
    return info
