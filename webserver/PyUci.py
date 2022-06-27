#!/usr/bin/python
""" PyUci.py - The HuCon queue class for log messages.

    Copyright (C) 2020 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""
import subprocess


class UciHelperBase(object):
    """
    Base helper class for handling configurations
    """

    def __init__(self, package=None):
        """
        Constructor
        :param package: String name of configuration to be read
        """
        self.config = {}
        try:
            self._read_config(package)
        except OSError:
            pass

    def _read_config(self, package=None):
        """
        Deserialize configurations into python dictionary structure
        :param package: Name of configuration file from /etc/config
        :return: None
        """
        self.config = {}
        command = ['uci', 'export'] if package is None else ['uci', 'export', package]
        settings = subprocess.check_output(command, encoding='utf-8')

        package_name = None
        config_type = None
        config_name = None
        value_dict = {}
        for line in settings.split('\n'):
            line = line.strip()
            if 'package' in line:
                # Get package name
                _, package_name = line.split(' ')
                # initialize new section in the config
                self.config.update({package_name: {}})
            elif 'config' in line:
                # split the line for config type and name
                line = line.split(' ', 2)
                config_type = line[1]
                config_name = None
                if len(line) == 3:
                    config_name = line[2].replace("'", "")
                # if the name is available: named list will be interpreted as dictionary
                if config_name:
                    if self.config[package_name].get(config_type, False):
                        # config_type already in dictionary, so use it
                        self.config[package_name][config_type].update({config_name: {}})
                    else:
                        # config_type is not in dictionary create new one
                        self.config[package_name].update({config_type: {config_name: {}}})
                # name not available: it is a list of configuration items
                else:
                    # Initialize new config list only if not already created
                    if not self.config[package_name].get(config_type, False):
                        self.config[package_name].update({config_type: []})
            elif 'option' in line:
                # create or update an option entry in value dictionary
                _, key, value = line.split(' ', 2)
                value = value.replace("'", "")
                value_dict.update({key: value})
            elif 'list' in line:
                # add an list value to option
                _, key, value = line.split(' ', 2)
                value = value.replace("'", "")
                # get a list if available, else create a new one
                value_list = value_dict.get(key, [])
                # append new value to list
                value_list.append(value)
                # create or update new option entry in value dictionary
                value_dict.update({key: value_list})
            elif line == '' and config_type is not None:
                # empty line between config blocks or packages
                # use it to append values to configuration entry
                if value_dict:
                    # Append value dictionary only if it is not empty
                    if config_name is not None:
                        # Add value dictionary to named list (dict)
                        if self.config[package_name].get(config_type, False):
                            # check if config_type already exists in the dictionary and use it
                            self.config[package_name][config_type].update({config_name: value_dict})
                        else:
                            # should normally not be, will override existing config_type item
                            self.config[package_name].update({config_type: {config_name: value_dict}})
                        # clear current name, may be the next config is a list not a dict
                        config_name = None
                    else:
                        # Configuration is a list
                        # Get the list from config if available else create new
                        config_list = self.config[package_name].get(config_type, [])
                        # append value to list
                        config_list.append(value_dict)
                        # update config with actual list
                        self.config[package_name].update({config_type: config_list})
                    # clear current config entry
                    config_type = None
                    # and value dictionary
                    value_dict = {}
            else:
                # line can not be interpreted ignore this
                pass


class WirelessHelper(UciHelperBase):
    """
    Helper class for handling wireless configuration of onion omega
    """

    def __init__(self, log):
        """
        Initialize super constructor with reading wireless configuration
        :param log: Logging Object
        """
        self._log = log
        super(WirelessHelper, self).__init__('wireless')

    def get_saved_wifi_networks(self):
        """
        Read and return a list with saved wifi networks
        :return: list
        """
        ret_list = []
        for wifi in self.config['wireless'].get('wifi-config', []):
            wifi['enabled'] = self.is_ssid_connected(wifi['ssid'])
            ret_list.append(wifi)
        return ret_list

    def add_wifi(self, ssid, key, encryption):
        """
        Add new wifi network to configuration
        :param ssid: str SSID
        :param key: str Password
        :param encryption: str Encryption
        :return: None
        """
        cmd = ['uci', 'add', 'wireless', 'wifi-config']
        self.__run_command(cmd)
        try:
            self.__set_wifi_on_index(ssid, encryption, key, -1)
            self.__uci_commit()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def move_wifi_up(self, ssid):
        """
        Move wifi network down in the priority list
        :param ssid: str SSID of moved Network
        :return: None
        """
        # find appropriate wifi network in the priority list
        for i, wifi in enumerate(self.config['wireless']['wifi-config']):
            if wifi['ssid'] == ssid:
                # if wifi network was found
                if i > 0:
                    # and can be moved up
                    # temporarily save information of previous wifi network
                    temp_ssid = self.config['wireless']['wifi-config'][i - 1]['ssid']
                    temp_encryption = self.config['wireless']['wifi-config'][i - 1]['encryption']
                    temp_key = self.config['wireless']['wifi-config'][i - 1]['key']
                    try:
                        # swap previous wifi network withe actual one
                        self.__set_wifi_on_index(temp_ssid, temp_encryption, temp_key, i)
                        self.__set_wifi_on_index(wifi['ssid'], wifi['encryption'], wifi['key'], i - 1)
                        self.__uci_commit()
                        break
                    except Exception as exc:
                        self.__uci_revert()
                        raise exc

    def move_wifi_down(self, ssid):
        """
        Move wifi network up in the priority list
        :param ssid: str SSID of moved Network
        :return: None
        """
        # find appropriate wifi network in the priority list
        for i, wifi in enumerate(self.config['wireless']['wifi-config']):
            if wifi['ssid'] == ssid:
                # if wifi network was found
                if i < len(self.config['wireless']['wifi-config']) - 1:
                    # and can be moved down
                    # temporarily save information of following wifi network
                    temp_ssid = self.config['wireless']['wifi-config'][i + 1]['ssid']
                    temp_encryption = self.config['wireless']['wifi-config'][i + 1]['encryption']
                    temp_key = self.config['wireless']['wifi-config'][i + 1]['key']
                    try:
                        # swap following wifi network withe actual one
                        self.__set_wifi_on_index(temp_ssid, temp_encryption, temp_key, i)
                        self.__set_wifi_on_index(wifi['ssid'], wifi['encryption'], wifi['key'], i + 1)
                        self.__uci_commit()
                        break
                    except Exception as exc:
                        self.__uci_revert()
                        raise exc

    def remove_wifi(self, ssid):
        """
        Remove wifi network from the priority list
        :param ssid: str SSID of removed Network
        :return: None
        """
        for i, wifi in enumerate(self.config['wireless']['wifi-config']):
            if wifi['ssid'] == ssid:
                cmd = ['uci', 'delete', 'wireless.@wifi-config[%d]' % i]
                try:
                    self.__run_command(cmd)
                    self.__uci_commit()
                except Exception as exc:
                    self.__uci_revert()
                    raise exc
                break

    def connect_wifi(self, ssid):
        """
        Connect to wifi network.
        :param ssid: str SSID of Network connect to
        :return: None
        """
        key, encryption = None, None
        # Get appropriate information for given ssid
        for i, wifi in enumerate(self.config['wireless']['wifi-config']):
            if wifi['ssid'] == ssid:
                ssid = wifi['ssid']
                key = wifi['key']
                encryption = wifi['encryption']
        # Connect only if everything available
        if ssid is not None and key is not None and encryption is not None:
            try:
                cmd = ['uci', 'set', 'wireless.sta.ssid=%s' % ssid]
                self.__run_command(cmd)
                cmd = ['uci', 'set', 'wireless.sta.key=%s' % key]
                self.__run_command(cmd)
                cmd = ['uci', 'set', 'wireless.sta.encryption=%s' % encryption]
                self.__run_command(cmd)
                self.__uci_commit()
                self.__restart_wifi()
            except Exception as exc:
                self.__uci_revert()
                raise exc

    def enable_sta_wifi(self):
        """
        Enable station Wifi Mode
        :return: None
        """
        try:
            cmd = ['uci', 'set', 'wireless.sta.disabled=%d' % 0]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def disable_sta_wifi(self):
        """
        Disable station Wifi Mode
        :return: None
        """
        try:
            cmd = ['uci', 'set', 'wireless.sta.disabled=%d' % 1]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def is_wifi_enabled(self):
        """
        Check if wifi sta mode is enabled
        :return: boolean True if enabled else False
        """
        return not bool(int(self.config['wireless']['wifi-iface']['sta']['disabled']))

    def is_wifi_disabled(self):
        """
        Check if wifi sta mode is disabled
        :return: boolean True if disabled else False
        """
        return bool(int(self.config['wireless']['wifi-iface']['sta']['disabled']))

    def get_ap_settings(self):
        """
        Reads needed configuration for parametrize WiFi AP Settings
        :return: dict Access Point Mode Settings
        """
        ret_dict = self.config['wireless']['wifi-iface']['ap']
        ip_addr = \
            subprocess.check_output(['uci', 'show', 'network.wlan.ipaddr'], encoding='utf-8').replace("'", '').strip().split(
                '=')[-1]
        ret_dict.update({'ap_ip_addr': ip_addr})
        return ret_dict

    def __set_wifi_on_index(self, ssid, encryption, key, index):
        """
        Puts WiFi network to given position in the priority list
        :param ssid: str WiFi SSID
        :param encryption: str WiFi Encryption
        :param key: str WiFi Password
        :param index: int Index
        :return: None
        """
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].ssid=%s' % (index, ssid)]
        self.__run_command(cmd)
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].key=%s' % (index, key)]
        self.__run_command(cmd)
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].encryption=%s' % (index, encryption)]
        self.__run_command(cmd)

    def __uci_commit(self):
        """
        Commits settings
        :return: None
        """
        cmd = ['uci', 'commit']
        self.__run_command(cmd)
        self._read_config('wireless')

    def __uci_revert(self):
        """
        Reverts settings
        :return: None
        """
        cmd = ['uci', 'revert', 'wireless']
        self.__run_command(cmd)
        self._read_config('wireless')

    def __restart_wifi(self):
        """
        Restart WiFi stack
        :return: None
        """
        cmd = ['wifi']
        self.__run_command(cmd)
        self._read_config('wireless')

    def __run_command(self, cmd):
        """
        Wraps command execution in to subprocess Popen and log it
        :param cmd: Command to be execute
        :return: None
        """
        proc = subprocess.Popen(cmd, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                self._log.put(output.strip())
        proc.poll()

    def enable_ap_wifi(self):
        """
        Enables Access Point WiFi Mode
        :return: None
        """
        try:
            cmd = ['uci', 'set', 'wireless.ap.disabled=%d' % 0]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception:
            self.__uci_revert()

    def disable_ap_wifi(self):
        """
        Disables Access Point WiFi Mode
        :return: None
        """
        try:
            cmd = ['uci', 'set', 'wireless.ap.disabled=%d' % 1]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def set_ap_settings(self, ssid, key, encryption, ip):
        """
        Configure Access Point Setting
        :param ssid: str SSID
        :param key: str Password
        :param encryption: str Encryption
        :param ip: str IP Address
        :return: None
        """
        try:
            cmd = ['uci', 'set', 'wireless.ap.ssid=%s' % ssid]
            self.__run_command(cmd)
            cmd = ['uci', 'set', 'wireless.ap.key=%s' % key]
            self.__run_command(cmd)
            cmd = ['uci', 'set', 'wireless.ap.encryption=%s' % encryption]
            self.__run_command(cmd)
            cmd = ['uci', 'set', 'network.wlan.ipaddr=%s' % ip]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    @classmethod
    def is_ssid_connected(cls, ssid):
        """
        Check if wifi with given ssid connected
        :param ssid: str SSID to check
        :return: boolean: True if connected else False
        """
        cmd = ['iwconfig']
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE, encoding='utf-8')
        for line in output.strip().split('\n'):
            if 'apcli0' in line:
                essid = line.split('ESSID:')[-1].strip().replace('"', "")
                if ssid == essid:
                    return True
                break
        return False
