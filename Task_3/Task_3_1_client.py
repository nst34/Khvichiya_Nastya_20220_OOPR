import socket
import time

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('localhost', 10000) # указали данные сервера, к которому надо подключиться
print('Подключение к {} порт {}'.format(*server_address))
sock.connect(server_address)

while True:
    # Отправка данных
    mess = 'Hello, world!'
    print(f'Отправка: {mess}')
    message = mess.encode()
    sock.sendall(message) # отправляет до тех пор, пока не закончатся данные для отправки
    
    time.sleep(1)