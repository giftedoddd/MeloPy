from threading import Thread, Lock, Condition
import socket as sock
import time

class Client:
    def __init__(self, ip="127.0.0.1", port=9353):
        self.__ip = ip
        self.__port = port
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)
        self.__default_interface = True
        self.__found_host = False
        self.__received_data = None
        self.__client_socket = None

    def __connect_to_host(self):
        try:
            with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as self.__client_socket:
                self.__client_socket.connect((self.__ip, self.__port))
        except Exception as e:
            print(e)

    def __find_host(self):
        with sock.socket(sock.AF_INET, sock.SOCK_DGRAM) as finder:
            finder.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
            finder.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEPORT, 1)
            finder.setsockopt(sock.SOL_SOCKET, sock.SO_BROADCAST, 1)
            finder.bind(("", 12345))

            timeout = 60
            while not self.__found_host:
                if timeout == 0:
                    self.__ip = "127.0.0.1"
                    self.__port = 9353
                    return

                message = finder.recv(512)
                self.__message_parser(message.decode("utf-8"))
                timeout -= 1
                time.sleep(1)

    def __message_parser(self, message):
        if "MeloPy" in message.split("\""):
            ip = message.split(":")[1].strip()
            port = message.split(":")[2]
            self.__found_host = True
            return ip, port

    def run(self):
        if not self.__default_interface:
            broadcast_thread = Thread(target=self.__find_host,
                                      daemon=True)
            broadcast_thread.start()
            broadcast_thread.join()

        self.__connect_to_host()

    def send_data(self, data):
        try:
            self.__client_socket.sendto(data.encode("utf-8"),
                                        (self.__ip, self.__port))
        except Exception as e:
            print(e)

    def receive_data(self):
        with self.__condition:
            while self.__received_data is None:
                self.__condition.wait()
            received = self.__received_data
            self.__received_data = None
        return received

    def close(self):
        self.__client_socket.close()
