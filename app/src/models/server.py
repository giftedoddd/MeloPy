from threading import Condition, Lock, Thread
import socket as so
import time

class Server:
    """
    Server based communication with available interfaces.
    """
    def __init__(self, port=9353, ip="127.0.0.1"):
        self.__ip = ip                              # Host's ip address.
        self.__port = port                          # Host's port address.
        self.__lock = Lock()                        # For Thread synchronizing.
        self.__condition = Condition(self.__lock)   # For Thread synchronizing.
        self.__interfaces = {}                      # A dictionary to keep sockets objects and their addresses.
        self.__found = False                        # A boolean variable to not broadcast everytime.
        self.__received_data = None                 # Stores received data from client

    def __len__(self):
        return len(self.__interfaces)

    def __repr__(self):
        return f"Server running at {self.__ip}:{self.__ip}"

    def __set_ip(self):
        """
        Sets host's ip address.\n
        Args: none
        Returns: none
        """
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
        """
        Sends a broadcast message to local network every 5 seconds.\n
        Args: none
        Returns: none
        """
        message = f"\"MeloPy\" UI join at: {self.__ip}:{self.__port}".encode("utf-8")

        with so.socket(so.AF_INET, so.SOCK_DGRAM) as broadcaster:
            try:
                broadcaster.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
                broadcaster.setsockopt(so.SOL_SOCKET, so.SO_REUSEPORT, 1)
                broadcaster.setsockopt(so.SOL_SOCKET, so.SO_BROADCAST, 1)
                broadcaster.bind(("", 12345))

                while not self.__found:
                    broadcaster.sendto(message, ("255.255.255.255", 12345))
                    time.sleep(2)

            except Exception as e:
                print(e)

    def __handle_client(self, client_socket, client_address):
        """
        Handles communication between host and client.\n
        Args: socket object, client ip address and port
        Returns: none
        """
        with client_socket:
            while True:
                received_data = client_socket.recv(1024).decode("utf-8")
                if not received_data:
                    continue
                with self.__lock:
                    self.__received_data = received_data
                    self.__condition.notify_all()

    def run(self):
        """
        Starts the server and accepts requests.\n
        Args: none
        Returns: none
        """
        with so.socket(so.AF_INET, so.SOCK_STREAM) as host_socket:
            host_socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
            host_socket.setsockopt(so.SOL_SOCKET, so.SO_REUSEPORT, 1)
            host_socket.bind((self.__ip, self.__port))
            host_socket.listen()

            while not self.__found:
                client_socket, client_address = host_socket.accept()
                self.__interfaces[client_address] = client_socket

                Thread(target=self.__handle_client,
                       args=(client_socket, client_address),
                       name=f"{client_address[0]}:{client_address[1]}",
                       daemon=True
                       ).start()

                if self.__found is False:
                    self.__found = True

    def add_interface(self):
        self.__ip = self.__set_ip()

        if self.__found is True:
            self.__found = False

        Thread(target=self.__broadcast,
               daemon=True).start()

        self.run()

    def receive_data(self):
        """
        Waits till receives data from client.\n
        Args: none
        Returns: str
        """
        with self.__condition:
            while self.__received_data is None:
                self.__condition.wait()
            received = self.__received_data
            self.__received_data = None
        return received

    def send_data(self, client_socket, to_address, message):
        """
        Send data to client or any other address provided.
        Args: socket object, (ip address, port), message
        Returns: none
        """
        client_socket.sendto(message.encode("utf-8"),
                             (to_address[0], to_address[1])
                             )

    def close(self):
        """
        Closes all available connections.
        Args: none
        Returns: none
        """
        if self.__interfaces:
            for socket in self.__interfaces.values():
                socket.close()
