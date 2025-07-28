from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .streams.UDPStream import UDPStream
from .streams.ROSStream import ROSStream
from .streams.Stream import Stream
import threading

class StreamManager:
    '''A factory class for stream objects; provides API endpoints'''
    # This class is a singleton
    instance = None
    def __init__(self):
        if StreamManager.instance:
            raise AttributeError(
                'Attempted to instantiate more than one instance of singleton'
                'class "StreamManager"'
            )
        self.router = APIRouter(prefix='/stream_manager', tags=['stream'])
        self.router.add_api_route('/create/udp', 
                                   self.create_udp_stream,
                                   methods=['POST'])
        self.router.add_api_route('/create/ros', 
                                   self.create_ros_stream,
                                   methods=['POST'])
        self.router.add_api_route('/get_streams',
                                  self.get_streams,
                                  methods=['GET'])
        self.streams = {}
        self.threads = {}
        StreamManager.instance = self

    def register_parser(self, parser, target_streams: list[str]):
        for s in target_streams:
            self.streams[s].register_parser(parser)

    class UDPRequest(BaseModel):
        name: str
        ip: str
        port: int
        recv_buffer: int | None
        parsers: list[str] | None

    async def create_udp_stream(self, request: UDPRequest):
        try:
            udp_stream = UDPStream(request.name, request.ip, request.port, 
            recv_buffer=request.recv_buffer if request.recv_buffer else 1024,
            parsers=request.parsers if request.parsers else [])
            await udp_stream.connect()
            if request.name in self.streams:
                raise ValueError(f'Stream with name {request.name} already '
                                 'exists!')    
            self.streams[request.name] = udp_stream
            return {'success': True}
        except Exception as e:
            raise HTTPException(400, str(e))
        
    class ROSRequest(BaseModel):
        name: str
        topic: str
        parsers: list[str]

    async def create_ros_stream(self, request: ROSRequest):
        try:
            if request.name in self.streams:
                raise ValueError(f'Stream with name {request.name} already '
                                 'exists!')    
            ros_stream = ROSStream(request.name,
                                   request.parsers,
                                   request.topic)
            self.streams[request.name] = ros_stream
            await ros_stream.connect()
            return {'success' : True}
        except Exception as e:
            raise HTTPException(400, str(e))
        
        
    async def get_streams(self):
        return {'streams' : [s.jsonify() for s in self.streams.values()]}
    
    async def loop(self):
        while True:
            s: Stream
            for s in self.streams.values():
                await s.listen()

