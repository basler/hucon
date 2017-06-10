try:
    import network
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
