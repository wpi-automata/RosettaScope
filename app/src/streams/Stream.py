from abc import ABC, abstractmethod
from ..parsers.Parser import Parser

class Stream(ABC):
    '''A Stream is an abstraction for a connection to a datastream from ROS,
    UDP, TCP, Serial...'''
    def __init__(self, name: str, parsers=[]):
        super().__init__()
        self.name = name
        self.stream_type = None  # defined by subclass
        self.parsers: list[Parser] = parsers  # Streams 

    @abstractmethod
    def connect(self):
        '''Connect to the data stream (eg open a socket)'''
        pass

    @abstractmethod
    def listen(self):
        '''Listen to the data stream and return a single frame'''
        pass

    def register_parser(self, parser: Parser):
        '''Adds a parser to this stream's list of parsers'''
        # Make sure not to double-add a parser!
        if parser in self.parsers:
            raise ValueError(f'Parser {parser} already in {self}\'s list of'
                             'parsers!')
        else:
            self.parsers.append(parser)

    def call_parsers(self, frame):
        '''Send the parsed frame to all subscribed parsers'''
        for parser in self.parsers:
            parser.process(frame)

    def loop(self):  # Should be executed in own thread
        frame = self.listen()
        self.call_parsers(frame)

    def jsonify(self):
        return {'name': self.name,
                'type': self.stream_type}