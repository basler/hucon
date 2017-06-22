import network
import time
import machine
import ubinascii
import neopixel

np = neopixel.NeoPixel(machine.Pin(14), 2)
np[0] = (0, 255, 0)
np[1] = (0, 0, 0)
np.write()

sta_if = network.WLAN(network.STA_IF)
network_found = False
for x in range(33):
    network_found = sta_if.isconnected()
    print('Network found: %s' % network_found)
    if network_found:
        break
    if np[0][1] == 255:
        np[0] = (0, 0, 0)
        np[1] = (0, 255, 0)
    else:
        np[0] = (0, 255, 0)
        np[1] = (0, 0, 0)
    np.write()
    time.sleep(0.3)

if network_found:
    np[0] = (255, 0, 0)
    np[1] = (255, 0, 0)
    np.write()
    time.sleep(1.0)
    np[0] = (0, 0, 0)
    np[1] = (0, 0, 0)
    np.write()

else:
    np[0] = (0, 255, 0)
    np[1] = (0, 255, 0)
    np.write()

    ap_if = network.WLAN(network.AP_IF)
    uid = ubinascii.hexlify(machine.unique_id()).decode()
    ap_if.config(essid='crawler-%s' % uid, authmode=network.AUTH_WPA_WPA2_PSK, password='hackerschool')
    print('Configured Network:\r\nAP: crawler-%s\r\nPASS: hackerschool\r\n' % uid)
