from app.src.streams.Stream import Stream
import socket

class UDPStream(Stream):
    def __init__(self, name: str, ip: str, port: int, recv_buffer=1024, parsers=[]):
        super().__init__(parsers)
        self._addr: tuple[str, int] = (ip, port)
        self._recv_buffer = 1024
        self._name = name
        self.stream_type = 'UDP'
        self.connect()

    # Properties and setters
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def addr(self):
        return self._addr
    
    @addr.setter
    def addr(self, new_addr):
        # Close socket before setting new socket address
        self.sock.close()
        self._addr = new_addr
        self.connect()  # Reconnect

    @property
    def ip(self):
        return self._addr[0]
    
    @ip.setter
    def ip(self, new_ip):
        self.addr = (new_ip, self.addr[1])

    @property
    def port(self):
        return self._addr[1]
    
    @port.setter
    def port(self, new_port):
        self.addr = (self.addr[0], new_port)
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(self._addr)

    def listen(self):
        source, data = self.sock.recvfrom(self._recv_buffer)
        return source, data
    
    def jsonify(self):
        return super().jsonify() | {
            'ip': self.ip,
            'port': self.port,
            'recv_buffer': self._recv_buffer
        }

