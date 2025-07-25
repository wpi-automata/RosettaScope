from app.src.streams.Stream import Stream
from app.src.parsers.Parser import Parser
import socket
import logging
import asyncio

class UDPStream(Stream):
    def __init__(self, name: str, ip: str, port: int, recv_buffer=1024, parsers=[]):
        super().__init__(parsers)
        self._addr: tuple[str, int] = (ip, port)
        self._recv_buffer = 1024
        self._name = name
        self.stream_type = 'UDP'
        # self.connect()
        self.logger = logging.getLogger('api')
        self.logger.setLevel(logging.DEBUG)
        self.udp_handler = UDPProtocol(self.parsers.copy())

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
    
    def register_parser(self, parser):
        super().register_parser(parser)
        self.udp_handler.add_parser(parser)
        print(f'registered parser: {parser.name} with stream {self.name}')
    
    async def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(self._addr)
        self.async_sock = await asyncio.get_event_loop().create_datagram_endpoint(
            lambda: self.udp_handler, sock=self.sock
        )

    async def listen(self):
        pass
    
    def jsonify(self):
        return super().jsonify() | {
            'ip': self.ip,
            'port': self.port,
            'recv_buffer': self._recv_buffer
        }


class UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, parsers:list[Parser]=[]):
        self.parsers: list[Parser] = parsers

    def add_parser(self, parser: Parser):
        self.parsers.append(parser)

    def datagram_received(self, data, addr):
        for p in self.parsers:
            p.process(data)

    def error_received(self, exc):
        raise exc
