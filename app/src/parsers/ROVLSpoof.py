from .Parser import Parser
import numpy as np
from tf_transformations import euler_from_quaternion
from stonefish_ros2.msg import BeaconInfo
import socket

class ROVLSpoof(Parser):
    def __init__(self, 
                 name: str, 
                 bind_ip: str,
                 bind_port: int,
                 output_ip: str,
                 output_port: int):
        super().__init__(name)
        self.type = 'rovlspoof'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.output_sock = (output_ip, output_port)
        self.sock.bind((self.bind_ip, self.bind_port))

    def process(self, frame: BeaconInfo):
        payload = self._make_nmea_payload(frame)
        checksum = self._calc_checksum(payload)
        nmea_msg = f'${payload}*{checksum}\r\n'
        print(f'msg: {nmea_msg}')
        self.output(nmea_msg)

    def output(self, frame: str):
        self.sock.sendto(bytes(frame, 'utf-8'),
                         self.output_sock)
        # print(frame)
    
    def _make_nmea_payload(self, msg: BeaconInfo):
        r, p, y = euler_from_quaternion([msg.local_orientation.w,
                                         msg.local_orientation.x,
                                         msg.local_orientation.y,
                                         msg.local_orientation.z])
        payload = ('USRTH,' # Command
                f'{np.rad2deg(msg.azimuth):.1f},'    # Apparent bearing in math degrees (ab)
                ','         # Apparent bearing in compass degrees (ac)
                f'{np.rad2deg(msg.elevation):.1f},'    # Apparent elevation (ae)
                f'{msg.range:.1f},'    # Slant range (sr)
                ','         # True bearing in math degrees (tb)
                ','         # True bearing in compass degrees (cb)
                f'{np.rad2deg(msg.elevation):.1f},'    # True elevation (te)
                f'{np.rad2deg(r):.1f},'     # Euler roll (er)
                f'{np.rad2deg(p):.1f},'      # Euler pitch (ep)
                f'{np.rad2deg(y):.1f},'    # Euler yaw (ey)
                ','         # Compass heading (ch)
                ','         # Analog gain in db (db)
                ','         # Autosync supported (ah)
                ','         # Autosync present (ag)
                ','         # Seconds since last autosync (ls)
                ','         # IMU status
                ','         # Channel (oc)
                ','         # Decoded ID (deprecated; idx)
                ''          # Queried ID (deprecated; idq)
                )
        return payload
    
    def _calc_checksum(self, payload: str) -> str:
        bytes = payload.encode('ascii')
        scan = bytes[0]
        for char in bytes[1:]:
            scan ^= char
        return f'{scan:x}'  # return checksum in hex w/o 0x @ front