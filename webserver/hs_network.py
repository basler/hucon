try:
    import network
    import machine
except:
    import socket

def get_ip_address():
    ip = '0.0.0.0'
    try:
        sta_if = network.WLAN(network.STA_IF)
        ip, _, _, _ = sta_if.ifconfig()
    except Exception as e:
        ip = str(socket.gethostbyname(socket.gethostname()))

    return ip

def set_wifi(ap_name: str, password: str):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ap_name, password)
    machine.reset()


def get_wifis() -> [str]:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    wpas = []

    for wpa in sta_if.scan():
        wpas = wpas + [wpa[0].decode('utf-8')]
    return wpas
