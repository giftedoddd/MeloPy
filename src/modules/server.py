from threading import Condition, Lock
import socket as so

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.command = None
        self.lock = Lock()
        self.condition = Condition(self.lock)
    # TODO:OK
    def start_server(self):
        with so.socket(so.AF_INET, so.SOCK_STREAM) as socket:
            socket.bind((self.ip, self.port))
            socket.listen()
            while True:
                client_socket, address = socket.accept()
                self.handle_client(client_socket)

    # TODO:OK
    def handle_client(self, client_socket):
        with client_socket:
            while True:
                command = client_socket.recv(1024).decode()
                if not command:
                    break
                with self.lock:
                    self.command = command
                    self.condition.notify_all()

    # TODO:NAILED IT
    def get_command(self):
        with self.condition:
            while self.command is None:
                self.condition.wait()
            command = self.command
            self.command = None
        return command
