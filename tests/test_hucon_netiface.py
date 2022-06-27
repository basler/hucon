""" Tests for webserver.HuConNetiface """
import subprocess
from unittest import TestCase
from unittest.mock import MagicMock

from webserver.HuConNetiface import get_info

class TestGetInfo(TestCase):
    def test_calls_ip_addr_show_command(self) -> None:
        run_subprocess_mock = _create_subprocess_run_mock(result_stdout="")
        get_info(
            interface_name="eth42",
            run_subprocess=run_subprocess_mock
        )
        run_subprocess_mock.assert_called_once_with(
            ["ip", "addr", "show", "eth42"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True
        )

    def test_neither_mac_nor_ip_found(self) -> None:
        run_subprocess_mock = _create_subprocess_run_mock(result_stdout="")
        info = get_info(
            interface_name="eth42",
            run_subprocess=run_subprocess_mock
        )
        self.assertIsNone(info.mac_address)
        self.assertIsNone(info.ipv4_address)

    def test_mac_extracted_from_link_line(self) -> None:
        run_subprocess_mock = _create_subprocess_run_mock(
            result_stdout="    link/ether 12:34:56:78:9a:bc brd ff:ff:ff:ff:ff:ff"
        )
        info = get_info(
            interface_name="eth42",
            run_subprocess=run_subprocess_mock
        )
        self.assertEqual(info.mac_address, "12:34:56:78:9a:bc")

    def test_ipv4_extracted_from_inet_line(self) -> None:
        run_subprocess_mock = _create_subprocess_run_mock(
            result_stdout="inet 192.168.1.2/24 brd 192.168.1.255 scope global dynamic noprefixroute eth42"
        )
        info = get_info(
            interface_name="eth42",
            run_subprocess=run_subprocess_mock
        )
        self.assertEqual(info.ipv4_address, "192.168.1.2")

def _create_subprocess_run_mock(result_stdout: str) -> MagicMock:
    result = subprocess.CompletedProcess(args="", returncode=0, stdout=result_stdout)
    return MagicMock(spec=subprocess.run, return_value=result)
