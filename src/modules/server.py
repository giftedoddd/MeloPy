from threading import Condition, Lock
import socket as so

class Server:
    """Server based communication between backend and frontend."""
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.command = None
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def start_server(self) -> None:
        """Starts server based on given ip address and port."""
        with so.socket(so.AF_INET, so.SOCK_STREAM) as socket:
            socket.bind((self.ip, self.port))
            socket.listen()
            while True:
                client_socket, address = socket.accept()
                self.handle_client(client_socket)

    def handle_client(self, client_socket:so) -> None:
        """Handles client commands."""
        with client_socket:
            while True:
                command = client_socket.recv(1024).decode()
                if not command:
                    break
                with self.lock:
                    self.command = command
                    self.condition.notify_all()

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
