import network
import time
import machine
import ubinascii

sta_if = network.WLAN(network.STA_IF)
network_found = False
for x in range(33):
    network_found = sta_if.isconnected()
    print('Network found: %s' % network_found)
    if network_found:
        break
    time.sleep(0.3)

if not network_found:
    ap_if = network.WLAN(network.AP_IF)
    uid = ubinascii.hexlify(machine.unique_id()).decode()
    ap_if.config(essid='crawler-%s' % uid, authmode=network.AUTH_WPA_WPA2_PSK, password='hackerschool')
    print('Configured Network:\r\nAP: crawler-%s\r\nPASS: hackerschool\r\n' % uid)

