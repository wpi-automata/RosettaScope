from abc import ABC, abstractmethod
from Stream import Stream

class Parser(ABC):
    '''A Parser consumes a Stream'''
    def __init__(self, stream: Stream):
        self.stream = stream
        super().__init__()

    def process(self, frame):  # This is the 'entrypoint' to a Parser
        '''Listen to frames from stream and process them'''
        self.output(frame)  # Default implementation is a pass-through

    @abstractmethod
    def output(self):
        '''Output parsed data'''
        pass