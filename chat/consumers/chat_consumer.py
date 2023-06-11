from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import json
import asyncio
import socket
import redis
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class PicoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("chat", self.channel_name)
        port_range = range(5555, 5560)
        port = None
        self.redis = redis.Redis(host='redis', port=6379, db=0)
        for p in port_range:
            self.lock = self.redis.lock(f'port:{p}')
            if self.lock.acquire(blocking=False):
                port = p
                break
        self.udp_task = asyncio.create_task(self.udp_receive_socket(port))
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "reply_channel": self.channel_name,
            "text": "Hello, world!",
            }))
        
    async def udp_receive_socket(self, port):
        logger.debug(f'port: {port}')
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('0.0.0.0',port))
        udp.setblocking(False)
        loop = asyncio.get_running_loop()
        while True:
            data, addr = await loop.sock_recvfrom(udp, 4096)
            logger.debug(data)

    async def disconnect(self, code):
        self.udp_task.cancel()
        self.lock.release()
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        logger.debug(text_data)
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "reply_channel": self.channel_name,
                "text": text_data,
            }
        )

    async def chat_message(self, event):
        if self.channel_name == event["reply_channel"]:
            return
        await self.send(text_data=event["text"])
