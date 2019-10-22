import subprocess
from copy import deepcopy
import json


class ConfigObject(object):
    def __init__(self, type, name=None):
        self.type = type
        self.name = name
        self.__option_dict = {}

    def get_option_dict(self):
        return self.__option_dict

    def add_option(self, key, value):
        self.__option_dict.update({key: value})

    def add_list_option(self, key, value):
        list_option = self.__option_dict.get(key, [])
        list_option.append(value)
        self.__option_dict.update({key: list_option})

    def get_option_value(self, key):
        return self.__option_dict.get(key, None)

    def __repr__(self):
        return json.dumps(self.__option_dict)

    def __getitem__(self, k):
        return self.__option_dict.__getitem__(k)


class ConfigPackage(object):
    def __init__(self, type):
        self.type = type
        self._config_objects = {}

    def add_config_object(self, config_object):
        co = self._config_objects.get(config_object.type, None)
        if co is None:
            self._config_objects.update({config_object.type: config_object})
        else:
            if isinstance(co, ConfigObject):
                self._config_objects.update({config_object.type: deepcopy([co, config_object])})
            else:
                co.append(config_object)
                self._config_objects.update({config_object.type: deepcopy(co)})

    def __repr__(self):
        return json.dumps(self._config_objects)

    def __getitem__(self, k):
        name = None
        if '.' in k:
            k, name = k.split('.')

        config_item = self._config_objects.__getitem__(k)

        if isinstance(config_item, list):
            if name is not None:
                for i in self._config_objects.__getitem__(k):
                    if i.name == name:
                        return i.get_option_dict()
            else:
                return [item.get_option_dict() for item in self._config_objects.__getitem__(k)]
        if isinstance(config_item, ConfigObject) :
            return config_item.get_option_dict()
        else:
            return config_item

    def get(self, key):
        return self._config_objects.get(key, None)


class UciHelperBase(object):
    def __init__(self, package=None):
        self.config = self._readconfig(package)

    def _readconfig(self, package):
        config = {}
        command = ['uci', 'export'] if package is None else ['uci', 'export', package]
        settings = subprocess.check_output(command).strip()
        conf_pack = None
        conf_obj = None
        for line in settings.split('\n'):
            if 'config' in line:
                if conf_obj is not None:
                    conf_pack.add_config_object(deepcopy(conf_obj))
                    conf_obj = None
                line = line.strip().split(' ')
                type = line[1]
                name = None
                if len(line) == 3:
                    name = line[2].replace("'", "")
                conf_obj = ConfigObject(type, name)
            elif 'option' in line:
                _, key, value = line.split(' ')
                value = value.replace("'", "")
                conf_obj.add_option(key, value)
            elif 'list' in line:
                _, key, value = line.split(' ')
                value = value.replace("'", "")
                conf_obj.add_list_option(key, value)
            elif 'package' in line:
                if conf_pack is not None:
                    config.update({pkg: deepcopy(conf_pack)})
                    conf_pack = None
                pkg, type = line.strip().split(' ')
                conf_pack = config.get(type, ConfigPackage(type))
            else:
                pass
        # last addings before ends
        conf_pack.add_config_object(deepcopy(conf_obj))
        config.update({conf_pack.type: deepcopy(conf_pack)})
        return config

    def __repr__(self):
        return str(self.config)


class WirelessHelper(UciHelperBase):
    def __init__(self, log):
        self._log = log
        super(WirelessHelper, self).__init__('wireless')

    def get_saved_wifi_networks(self):
        conf_obj = self.config['wireless'].get('wifi-config')
        print(conf_obj)
        if conf_obj is None:
            return []
        if isinstance(conf_obj, list):
            return conf_obj
        else:
            return [conf_obj]

    def add_wifi(self, ssid, key, encryption):
        cmd = ['uci', 'add', 'wireless', 'wifi-config']
        self.__run_command(cmd)
        try:
            self.__set_wifi_on_index(ssid, encryption, key, -1)
            self.__uci_commit()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def move_wifi_up(self, ssid):
        if isinstance(self.config['wireless']['wifi-config'], list):
            for i, wifi in enumerate(self.config['wireless']['wifi-config']):
                if wifi['ssid'] == ssid:
                    if i > 0:
                        temp_ssid = self.config['wireless']['wifi-config'][i-1]['ssid']
                        temp_encryption = self.config['wireless']['wifi-config'][i-1]['encryption']
                        temp_key = self.config['wireless']['wifi-config'][i-1]['key']
                        try:
                            self.__set_wifi_on_index(temp_ssid, temp_encryption, temp_key, i)
                            self.__set_wifi_on_index(wifi['ssid'], wifi['encryption'], wifi['key'], i-1)
                            self.__uci_commit()
                            break
                        except Exception as exc:
                            self.__uci_revert()
                            raise exc

    def move_wifi_down(self, ssid):
        if isinstance(self.config['wireless']['wifi-config'], list):
            for i, wifi in enumerate(self.config['wireless']['wifi-config']):
                if wifi['ssid'] == ssid:
                    if i < len(self.config['wireless']['wifi-config'])-1:
                        temp_ssid = self.config['wireless']['wifi-config'][i+1]['ssid']
                        temp_encryption = self.config['wireless']['wifi-config'][i+1]['encryption']
                        temp_key = self.config['wireless']['wifi-config'][i+1]['key']
                        try:
                            self.__set_wifi_on_index(temp_ssid, temp_encryption, temp_key, i)
                            self.__set_wifi_on_index(wifi['ssid'], wifi['encryption'], wifi['key'], i+1)
                            self.__uci_commit()
                            break
                        except Exception as exc:
                            self.__uci_revert()
                            raise exc

    def remove_wifi(self, ssid):
        if isinstance(self.config['wireless']['wifi-config'], list):
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
        else:
            if self.config['wireless']['wifi-config']['ssid'] == ssid:
                cmd = ['uci', 'delete', 'wireless.@wifi-config[0]']
                try:
                    self.__run_command(cmd)
                    self.__uci_commit()
                except Exception as exc:
                    self.__uci_revert()
                    raise exc

    def connect_wifi(self, ssid):
        ssid, key, encryption = None, None, None
        if isinstance(self.config['wireless']['wifi-config'], list):
            for i, wifi in enumerate(self.config['wireless']['wifi-config']):
                if wifi['ssid'] == ssid:
                    ssid = wifi['ssid']
                    key = wifi['key']
                    encryption = wifi['encryption']
        else:
            if self.config['wireless']['wifi-config']['ssid'] == ssid:
                ssid = self.config['wireless']['wifi-config']['ssid']
                key = self.config['wireless']['wifi-config']['key']
                encryption = self.config['wireless']['wifi-config']['encryption']
        if ssid is not None and key is not None and encryption is not None:
            try:
                cmd = ['uci', 'set', 'wireless.sta.ssid=%s' % ssid]
                self.__run_command(cmd)
                cmd = ['uci', 'set', 'wireless.sta.key=%s' % key]
                self.__run_command(cmd)
                cmd = ['uci', 'set', 'wireless.sta.encryption=%s' % encryption]
                self.__run_command(cmd)
                self.__run_command()
            except Exception as exc:
                self.__uci_revert()
                raise exc

    def enable_sta_wifi(self):
        try:
            cmd = ['uci', 'set', 'wireless.sta.disabled=%d' % 0]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def disable_sta_wifi(self):
        try:
            cmd = ['uci', 'set', 'wireless.sta.disabled=%d' % 1]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def restart_wifi(self):
        self.__run_command(['wifi'])

    def is_wifi_enabled(self):
        return not bool(int(self.config['wireless']['wifi-iface.sta']['disabled']))

    def is_wifi_disabled(self):
        return bool(int(self.config['wireless']['wifi-iface.sta']['disabled']))

    def get_ap_settings(self):
        ret_dict = self.config['wireless']['wifi-iface.ap']
        ip_addr = subprocess.check_output(['uci', 'show', 'network.wlan.ipaddr']).replace("'", '').decode().strip().split('=')[-1]
        ret_dict.update({'ap_ip_addr': ip_addr})
        return ret_dict

    def __set_wifi_on_index(self, ssid, encryption, key, index):
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].ssid=%s' % (index, ssid)]
        self.__run_command(cmd)
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].key=%s' % (index, key)]
        self.__run_command(cmd)
        cmd = ['uci', 'set', 'wireless.@wifi-config[%d].encryption=%s' % (index, encryption)]
        self.__run_command(cmd)

    def __uci_commit(self):
        cmd = ['uci', 'commit']
        self.__run_command(cmd)
        self.config = self._readconfig('wireless')

    def __uci_revert(self):
        cmd = ['uci', 'revert', 'wireless']
        self.__run_command(cmd)
        self.config = self._readconfig('wireless')

    def __restart_wifi(self):
        cmd = ['wifi']
        self.__run_command(cmd)
        self.config = self._readconfig('wireless')

    def __run_command(self, cmd):
        # print cmd
        proc = subprocess.Popen(cmd, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                self._log.put(output.strip())
        proc.poll()

    def enable_ap_wifi(self):
        try:
            cmd = ['uci', 'set', 'wireless.ap.disabled=%d' % 0]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception:
            self.__uci_revert()

    def disable_ap_wifi(self):
        try:
            cmd = ['uci', 'set', 'wireless.ap.disabled=%d' % 1]
            self.__run_command(cmd)
            self.__uci_commit()
            self.__restart_wifi()
        except Exception as exc:
            self.__uci_revert()
            raise exc

    def set_ap_settings(self, ssid, key, encryption, ip):
        # ToDo improve implementation here
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


if __name__ == '__main__':
    from HuConLogMessage import HuConLogMessage
    _log = HuConLogMessage()
    uh = WirelessHelper(_log)
    # print(json.dumps(uh.config['wireless']['wifi-config.ap']))
    # uh.add_wifi('test2', 'psk2', 'test')
    # print(uh.config['wireless']['wifi-config'])
    # uh.move_wifi_up('test2')
    print(uh.get_saved_wifi_networks())