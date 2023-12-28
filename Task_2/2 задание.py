class Server:
    ip = 0

    def __init__(self):
        self.buffer = []
        self.ip = Server.ip + 1
        Server.ip += 1
        self.router = None

    def send_data(self, data): #отправка даты
        self.router.buffer.append(data)
        self.buffer = []

    def get_data(self): #возвращает то, что хранилось в буфере и отчищает его
        self.buffer_out = self.buffer.copy()
        self.buffer.clear()
        return self.buffer_out

    def get_ip(self): #просто возвращает ip
        return self.ip


class Router:
    def __init__(self):
        self.buffer = []
        self.linked = {}

    def link(self, server): #подсоединяет сервер к роутеру
        server.router = self
        self.linked[f'{server.ip}'] = server

    def unlink(self, server): #отсоединяет сервер от роутера
        server.router = None
        self.linked.pop(f'{server.ip}')

    def send_data(self): #отправляет содержимое буфера
        for pack in self.buffer:
            if self.linked.get(str(pack.ip)) is not None:
                self.linked.get(str(pack.ip)).buffer.append(pack)
        self.buffer = []

class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip

 # проверки
assert hasattr(Router, 'link') and hasattr(Router, 'unlink') and hasattr(Router, 'send_data'), "в классе Router присутсвутю не все методы, указанные в задании"
assert hasattr(Server, 'send_data') and hasattr(Server, 'get_data') and hasattr(Server, 'get_ip'), "в классе Server присутсвутю не все методы, указанные в задании"

router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()
assert len(router.buffer) == 0, "после отправки сообщений буфер в роутере должен очищаться"
assert len(sv_from.buffer) == 0, "после получения сообщений буфер сервера должен очищаться"
assert len(msg_lst_to) == 2, "метод get_data вернул неверное число пакетов"
assert msg_lst_from[0].data == "Hi" and msg_lst_to[0].data == "Hello", "данные не прошли по сети, классы не функционируют должным образом"
assert hasattr(router, 'buffer') and hasattr(sv_to, 'buffer'), "в объектах классов Router и/или Server отсутствует локальный атрибут buffer"
router.unlink(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
router.send_data()
msg_lst_to = sv_to.get_data()
assert msg_lst_to == [], "метод get_data() вернул неверные данные, возможно, неправильно работает метод unlink()"


# serv1 = Server()
# serv2 = Server()
# router1 = Router()
#
# router1.link(serv1)
# router1.link(serv2)
#
# serv1.send_data(Data("Hello", serv2.get_ip()))
# serv2.send_data(Data("Hi", serv1.get_ip()))
# router1.send_data()
# received_data1 = serv1.get_data()
# received_data2 = serv2.get_data()
# print(f'serv1 received {received_data1[0].data}, serv2 received {received_data2[0].data}')