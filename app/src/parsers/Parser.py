from abc import ABC, abstractmethod

class Parser():
    '''A Parser consumes a Stream'''
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def process(self, frame):  # This is the 'entrypoint' to a Parser
        '''Listen to frames from stream and process them'''
        self.output(frame)  # Default implementation is a pass-through

    def output(self, frame):
        '''Output parsed data'''
        print(str(frame))