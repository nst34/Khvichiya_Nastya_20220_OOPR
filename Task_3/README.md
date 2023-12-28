# Khvichiya_Nastya_20220_OOPR

Task_3:
TCP Client-streaming (Клиент, например, раз в 1 секунду отправляет данные на сервер), используя встроенный в Python модуль socket.
Task_3_1_server.py Task_3_1_client.py Используя encode() и decode()
Task_3_2_server.py Task_3_2_client.py Используя pickle - де/сериализация произвольных объектов.
Task_3_3_server.py Task_3_3_client.py Используя Google Protocol Buffers - де/сериализация определенных структурированных данных, а не произвольных объектов Python

Task_3_1_client.py

```python
import socket
import time

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
    message = mess.encode()
    sock.sendall(message) # отправляет до тех пор, пока не закончатся данные для отправки
    
    time.sleep(1)
```
![Client_1](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/клиент%203.1.png)

Task_3_1_server.py
```python
import socket

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ('localhost', 10000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen()

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями и ретранслируем их
        while True:
            data = connection.recv(16)
            print(f'Получено: {data.decode()}')
            if data:
                print('Обработка данных...')
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        pass
```
![Server_1](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/сервер%203.1.png)


Task_3_2_client.py
```python
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
```
![Client_2](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/клиент%203.2.png)

Task_3_2_server.py
```python
import socket
import pickle

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ('localhost', 10000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen()

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями и ретранслируем их
        while True:
            data = connection.recv(4096)
            with open('3_2_server.pickle', 'wb') as f:
                f.write(data)
            with open('3_2_server.pickle', 'rb') as f:
                data = pickle.load(f)
            
            print(f'Получено: {data}')
            if data:
                print('Обработка данных...')
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        pass
```
![Server_2](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/сервер%203.2.png)


Task_3_3_client.py
```python
import temp_pb2
import socket
import time
import sys

HOST = '127.0.0.1'
PORT = 8888
s = None

temp = temp_pb2.TempEvent()

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print("Couldn't connect to server")
    sys.exit(1)

with s:
    while True:
        temp.device_id = 1
        temp.event_id = 2
        temp.humidity = 3
        temp.video_data = 4
        s.sendall(temp.SerializeToString())
        print(f"send:\n{temp}")
        time.sleep(1)    
```
![Client_3](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/клиент%203.3.png)

Task_3_3_server.py
```python
import socket
import temp_pb2
import sys

HOST = "127.0.0.1"
PORT = 8888
s = None

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print("There's no client")
    sys.exit(1)

conn, addr = s.accept()
temp = temp_pb2.TempEvent()

with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        temp.ParseFromString(data)
        print(f"device_id: {temp.device_id}, event_id: {temp.event_id}, humidity: {temp.humidity}, video_data: {temp.video_data}")
```
![Server_3](https://github.com/nst34/Khvichiya_Nastya_20220_OOPR/blob/main/Task_3/image/сервер%203.3.png)