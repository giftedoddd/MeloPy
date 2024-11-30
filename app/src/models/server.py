from threading import Condition, Lock, Thread
import socket as so

class Server:
    """
    Server based communication with available interfaces.
    """
    def __init__(self, ip, port, interfaces=1):
        self.__ip = ip
        self.__port = port
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)
        self.__command = None
        self.__interfaces = interfaces

    def __repr__(self):
        return f"Server running at {self.__ip}:{self.__ip}"

    def run(self) -> None:
        """
        Starts server based on given ip address and port.
        """
        with so.socket(so.AF_INET, so.SOCK_STREAM) as socket:
            socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
            socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEPORT, 1)
            socket.bind((self.__ip, self.__port))
            socket.listen(self.__interfaces)
            while True:
                client_socket, address = socket.accept()
                self.handle_client(client_socket)

    def handle_client(self, client_socket:so) -> None:
        """Handles client commands."""
        try:
            with client_socket:
                while True:
                    command = client_socket.recv(1024).decode()
                    if not command:
                        break
                    with self.lock:
                        self.command = command
                        self.condition.notify_all()
        except Exception as e:
            print(e)
            client_socket.close()

    def get_command(self):
        """Looking for if there is any command from client if not it will wait for commands."""
        with self.condition:
            while self.command is None:
                self.condition.wait()
            command = self.command
            self.command = None
        return command

    def set_tmp_command(self, command:str) -> None:
        """Used to play next song after finishing current one."""
        with self.lock:
            self.command = command
            self.condition.notify_all()
