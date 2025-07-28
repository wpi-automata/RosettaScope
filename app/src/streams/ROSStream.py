import rclpy.subscription
from .Stream import Stream
from ..parsers.Parser import Parser
import rclpy
from rclpy.node import Node
import rclpy.callback_groups
import rclpy.executors
from tf_transformations import euler_from_quaternion
from stonefish_ros2.msg import BeaconInfo
import numpy as np
import asyncio
import threading

class ROSStream(Stream):
    NAMESPACE = 'rosetta_scope'
    cb_group = None
    executor = None
    def __init__(self, name, parsers, topic):
        super().__init__(name, parsers)
        self.stream_type = 'ROS2'
        self.topic = topic
        # TODO: Add type 
        rclpy.init()
        if not ROSStream.cb_group:
            ROSStream.cb_group = rclpy.callback_groups.ReentrantCallbackGroup()
        self.node = ROSNode(name, 
                            ROSStream.NAMESPACE, 
                            topic,
                            ROSStream.cb_group,
                            self.parsers)
        

    async def connect(self):
        if not ROSStream.executor:
            ROSStream.executor = rclpy.executors.MultiThreadedExecutor()
        # Spin in a new thread; maybe there is a better way to do this
        s = lambda: rclpy.spin(self.node, ROSStream.executor)
        self.thr = threading.Thread(target=s, daemon=True)
        self.thr.start()

    def listen(self):
        pass
        
    def register_parser(self, parser: Parser):
        super().register_parser(parser)
        self.node.register_parser(parser)

    def jsonify(self):
        return super().jsonify() | {
            'topic' : self.topic
        }

class ROSNode(Node): 
    def __init__(self, 
                 node_name: str, 
                 namespace: str, 
                 topic: str, 
                 cb_group: rclpy.callback_groups.CallbackGroup, 
                 parsers: list[Parser]=[]):
        super().__init__(node_name, namespace=namespace)
        self.namespace = namespace
        self.topic = topic
        self.parsers = parsers
        self.subscriber = self.create_subscription(BeaconInfo, 
                                                   topic, 
                                                   self._cb,
                                                   1,
                                                   callback_group=cb_group)
    def _cb(self, msg: BeaconInfo):
        for p in self.parsers:
            p.process(msg)

    def register_parser(self, parser: Parser):
        self.parsers.append(parser)
    

    
    
