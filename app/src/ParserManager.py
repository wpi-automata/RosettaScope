from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .parsers.Parser import Parser
from .parsers.ROVLSpoof import ROVLSpoof
from .StreamManager import StreamManager
class ParserManager:
    '''A factory class for parrsers; provides API endpoitns'''
    instance = None
    def __init__(self, stream_manager: StreamManager):
        if ParserManager.instance:
            raise AttributeError(
                'Attempted to instantiate more than one instance of singleton'
                'class "ParserManager"'
            )
        self.stream_manager = stream_manager
        self.router = APIRouter(prefix='/parser_manager', tags=['parser'])
        self.router.add_api_route('/create', 
                                  self.create_parser, 
                                  methods=['POST'])
        self.router.add_api_route('/get_parsers',
                                  self.get_parsers,
                                  methods=['GET'])
        self.parsers = {}
        ParserManager.instance = self

    class CreateParserRequest(BaseModel):
        name: str
        type: str
        streams: list[str]
        bind_ip: str | None
        bind_port: int | None
        output_ip: str | None
        output_port: int | None

    async def create_parser(self, request: CreateParserRequest):
        try:
            if request.name in self.parsers:
                raise ValueError(f'Parser named {request.name} already exists')
            match request.type:
                case '':
                    parser = Parser(request.name)
                    self.stream_manager.register_parser(parser, 
                                                        request.streams)
                    self.parsers[request.name] = parser
                    return {'success' : True}
                case 'rovlspoof':
                    parser = ROVLSpoof(request.name,
                                       request.bind_ip,
                                       request.bind_port,
                                       request.output_ip,
                                       request.output_port)
                    self.stream_manager.register_parser(parser, 
                                                        request.streams)
                    self.parsers[request.name] = parser
                    return {'success' : True}
                case _:
                    raise ValueError(f'{request.type} is not a valid type of '
                                     'parser.')
        except Exception as e:
            raise HTTPException(400, str(e))
        
    async def get_parsers(self):
        # raise HTTPException(501, 'not implemented :(')
        return {'parsers' : [p.jsonify() for p in self.parsers.values()]}