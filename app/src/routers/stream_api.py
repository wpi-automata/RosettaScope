from fastapi import APIRouter
from ..streams.UDPStream import UDPStream

router = APIRouter(prefix='/stream_factory')

@router.post('/udp', tags=['Streams'])
def create_udp_router(msg):
    print(msg)