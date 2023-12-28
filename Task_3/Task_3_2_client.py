import socket
import time
import pickle

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('localhost', 10000) # указали данные сервера, к которому надо подключиться
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)

while True:
    # Отправка данных
    mess = 'Hello, world!'
    print(f'Отправка: {mess}')
    with open('3_2_client.pickle', 'wb') as f:
        pickle.dump(mess, f)
    with open('3_2_client.pickle', 'rb') as f:
        sock.sendall(f.read())
    
    time.sleep(10)