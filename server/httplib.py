import threading
import urllib.parse
import socket
import json


class ConstructResponse:
    """ Составляет HTTP ответ """
    STATUS_OK = "200 OK"
    STATUS_REQUEST_ERROR = "400"
    STATUS_SERVER_INTERNAL = "500"

    def __init__(self):
        self.version = "HTTP/1.1"
        self.status_code = ConstructResponse.STATUS_SERVER_INTERNAL
        self.body = {}

    def convert_to_bytes(self):
        result = f"{self.version} {self.status_code}\r\n\r\n"
        result += json.dumps(self.body)

        return result.encode()


class ValveHTTPRequestsHandler:
    """ Реализация HTTP сервера, который обрабатывает тело в JSON
     формате, формирует и отправляет ответ при помощи класса ConstructResponse
    """
    def __init__(self, host: str = "", port: int = 9091):
        self.MAX_CONNECTIONS = 80
        self.BUFF_SIZE = 1024 * 16   # 16KB на прием сообщений
        self.__thread = None         # Для демонизации процесса приема сообщений
        self.__is_daemon = False     # Флаг работы потока
        self.__host = host
        self.__port = port
        self.__handlers = {}

    def run(self) -> None:
        """ Запускает демонизированный обработчик __handle_requests """
        self.__is_daemon = True
        self.__thread = threading.Thread(target=self.__handle_requests)
        self.__thread.start()

    def stop(self) -> None:
        """ Останавливает выделенный для прослушивания подключений поток """
        self.__is_daemon = False

    def add_handler(self, op_type: str, handler: object) -> None:
        """ Добавляет обработчик в список обработчиков """
        self.__handlers[op_type] = handler

    def __handle_requests(self) -> None:
        """ Начинает прослушивание порта self.__port, принимает подключение
         от клиентов. Основная задача метода - распознание операций, которые
         хочет исполнить клиент при помощи списка обработчиков self.__handlers,
         который реализуется функциями
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.__host, self.__port))
        server.listen(self.MAX_CONNECTIONS)

        while self.__is_daemon:
            connection, address = server.accept()
            raw_request = connection.recv(self.BUFF_SIZE).decode()
            url_unencoded_data = urllib.parse.unquote(raw_request.split("jsonRequestData=")[1])
            json_data = json.loads(url_unencoded_data)

            try:
                operation_type = json_data["op_type"]

                response = ConstructResponse()
                response.body = self.__handlers[operation_type](json_data)
                print(response.body)
                response.status_code = ConstructResponse.STATUS_OK

                connection.send(response.convert_to_bytes())
            except KeyError:
                response = ConstructResponse()
                response.status_code = ConstructResponse.STATUS_REQUEST_ERROR

                connection.send(response.convert_to_bytes())

            connection.close()
