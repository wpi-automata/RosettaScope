from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .parsers.Parser import Parser
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

    async def create_parser(self, request: CreateParserRequest):
        try:
            match request.type:
                case '':
                    parser = Parser(request.name)
                    self.stream_manager.register_parser(parser, 
                                                        request.streams)
                    return {'success' : True}
                case _:
                    raise ValueError(f'{request.type} is not a valid type of '
                                     'parser.')
        except Exception as e:
            raise HTTPException(400, str(e))
        
    async def get_parsers(self):
        raise HTTPException(501, 'not implemented :(')