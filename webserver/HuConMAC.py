#!/usr/bin/python
""" HuConMAC.py - Get MAC address from Onion Omega2

    Copyright (C) 2020 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""
import subprocess
import string


_MAC_ADDRESS_REGISTERS = (4, 6, 8)

def get_mac_address(): # type: () -> str
    """ Get MAC address of ra0 interface """
    register_dump = _get_iwpriv_dump()
    reg_swapped_values = [
        register_dump.get_reg_swapped_str(reg)
        for reg in _MAC_ADDRESS_REGISTERS
    ]
    mac_address = "".join(reg_swapped_values)
    return mac_address


def _get_iwpriv_dump(): # type: () -> RegisterDump
    """ Get wireless chip register dump using `iwpriv` """
    cmd = ['iwpriv', 'ra0', 'e2p']
    dump_str = subprocess.check_output(cmd, universal_newlines=False).decode('utf-8')
    dump = _IwprivRegisterDump(dump_str)
    return dump


class _IwprivRegisterDump(object):
    """ Dump of wireless chip registers """
    def __init__(self, dump): # type: (str) -> None
        """ Init dump from string """
        self._registers = self._parse_dump(dump)

    def get_reg_swapped_str(self, addr): # type (int) -> str
        """ Get register value as str with bytes swapped """
        raw = self._registers[addr]
        swapped = raw[2:] + raw[:2]
        return swapped

    def _parse_dump(self, dump): # type: (str) -> Dict[str, str]
        """ Parse register dump """
        lines = dump.splitlines()[1:] # first line is "ra0 e2p"
        reg_entries = [entry for line in lines for entry in line.split()]
        reg_addr_value_pairs = [
            reg_entry.partition(':')[::2] # first and third element
            for reg_entry in reg_entries
        ]
        registers = {
            self._parse_addr(raw_addr): self._parse_raw_value(raw_value)
            for raw_addr, raw_value in reg_addr_value_pairs
        }
        return registers

    def _parse_addr(self, addr): # type: (str) -> int
        """ Parse hex addr in format [0x1234] """
        format_ok = all((
            len(addr) >= 4,
            addr[:3] == '[0x',
            addr[-1] == ']',
            _is_hex_digit(addr[3:-1])
        ))
        if not format_ok:
            raise ValueError('bad address: {}'.format(addr))
        addr_int = int(addr[3:-1], 16)
        return addr_int

    def _parse_raw_value(self, raw_value): # type: (str) -> str
        """ Parse raw register value (in format 4 hexdigits) """
        format_ok = (
            len(raw_value) == 4 and
            _is_hex_digit(raw_value)
        )
        if not format_ok:
            raise ValueError('bad register value: {}'.format(raw_value))
        return raw_value


def _is_hex_digit(s): # type: (str) -> bool
    """ Check whether a string consists of hexadecimal digits """
    result = all(c in string.hexdigits for c in s)
    return result
