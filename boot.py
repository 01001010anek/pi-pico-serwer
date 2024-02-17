import network
import socket
import time
from machine import Pin

# Inicjalizacja diody LED
led = Pin(15, Pin.OUT)

# Konfiguracja sieci Wi-Fi
ssid = 'Nazwa_twojej_sieci_WiFi'
password = 'Hasło_do_twojej_sieci_WiFi'

# Połączenie z siecią Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Szablon strony HTML
html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Strona hostowana przez Raspberry Pi Pico</title>
</head>
<body>
%s
</body>
</html>
"""

# Czekaj na połączenie z siecią Wi-Fi
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Czekanie na połączenie...')
    time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError('Nie udało się połączyć z siecią WiFi')
else:
    print('Połączono z siecią WiFi')
    status = wlan.ifconfig()
    print('Adres IP:', status[0])

# Adres i port serwera HTTP
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

# Inicjalizacja gniazda serwera
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Nasłuchiwanie na', addr)

# Nasłuchiwanie na połączenia
while True:
    try:
        cl, addr = s.accept()
        print('Klient połączony z', addr)
        request = cl.recv(1024)
        print('Żądanie:', request)

        # Odpowiedź na żądanie
        response = html % open('index.html').read()

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Zamknięto połączenie')
