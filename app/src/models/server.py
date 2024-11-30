from threading import Condition, Lock, Thread
import socket as so
import time

class Server:
    """
    Server based communication with available interfaces.
    """
    def __init__(self, port=9353, ip="127.0.0.1"):
        self.__ip = ip
        self.__port = port
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)
        self.__interfaces = {}
        self.__default_interface = True
        self.__found = False
        self.__received_data = None

    def __len__(self):
        return len(self.__interfaces)

    def __repr__(self):
        return f"Server running at {self.__ip}:{self.__ip}"

    def __set_ip(self):
        if self.__default_interface:
            return

        try:
            with so.socket(so.AF_INET, so.SOCK_DGRAM) as connection:
                connection.settimeout(2)
                connection.connect(("1.1.1.1", 80))
                ip = connection.getsockname()
                if ip[0].startswith("127"):
                    return "127.0.0.1"
                return ip[0]
        except OSError as e:
            print(e)
        except Exception as e:
            print(e)

    def __broadcast(self):
        message = f"\"MeloPy\" UI join at: {self.__ip}:{self.__port}".encode("utf-8")

        with so.socket(so.AF_INET, so.SOCK_DGRAM) as broadcaster:
            try:
                broadcaster.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
                broadcaster.setsockopt(so.SOL_SOCKET, so.SO_REUSEPORT, 1)
                broadcaster.bind(("", 12345))

                while not self.__found:
                    broadcaster.sendto(message, ("255.255.255.255", 12345))
                    time.sleep(5)

            except Exception as e:
                print(e)

    def __handle_client(self, client_socket, client_address):
        with client_socket:
            while True:
                received_data = client_socket.recv(1024).decode("utf-8")
                if not received_data:
                    continue
                with self.__lock:
                    self.__received_data = received_data
                    self.__condition.notify_all()

    def run(self):
        self.__set_ip()

        if not self.__default_interface:
            Thread(target=self.__broadcast,
                   daemon=True).start()



        with so.socket(so.AF_INET, so.SOCK_STREAM) as socket:
            socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
            socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEPORT, 1)
            socket.bind((self.__ip, self.__port))
            socket.listen()