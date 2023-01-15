import enum
import json
import struct
import traceback
import zlib
from typing import Dict, Iterable, List, Union

import websockets

from .api_client import RoomInfo


@enum.unique
class PacketType(enum.Enum):
    HEARTBEAT = 2  #客户端发送的心跳包
    POPULARITY = 3 #人气 心跳包回复
    COMMAND = 5  #消息
    ENTER_ROOM = 7 #认证加入房间
    ENTER_ROOM_RESPONSE = 8 #服务端发送的心跳包，客户端接收到此信息时需要返回一个心跳包


class Packet:
    def __init__(self, packet_type: PacketType, content: Union[int, str], short_tag: int = 1, tag: int = 1):
        self._short_tag = short_tag
        self.packet_type = packet_type
        self._tag = tag
        self.content = content

    @classmethod
    def EnterRoom(cls, room: RoomInfo) -> "Self":
        return Packet(PacketType.ENTER_ROOM, json.dumps({
            "uid": room.user_id,
            "roomid": room.room_id,
            "protover": 0,
        }, ensure_ascii=False))

    @classmethod
    def HeartBeat(cls) -> "Self":
        return Packet(PacketType.HEARTBEAT, "[object Object]")

    @classmethod
    def parse_one(cls, message: bytes, offset=0) -> "Self":
        (total_length, header_length, short_tag, packet_type,
         tag) = struct.unpack_from(">ihhii", message, offset)
        content_start = offset + header_length
        content_end = offset + total_length
        content = message[content_start:content_end]
        return Packet(PacketType(packet_type), content, short_tag, tag)

    @classmethod
    def parse(cls, message: bytes) -> Iterable["Self"]:
        offset = 0
        msg_length = len(message)
        while offset + 16 < msg_length:
            packet = cls.parse_one(message, offset)
            offset += 16 + len(packet.content)
            if packet._short_tag == 2:
                yield from cls.parse(zlib.decompress(packet.content))
            elif packet.packet_type == PacketType.POPULARITY:
                packet.content = struct.unpack(">i", packet.content)
                yield packet
            else:
                packet.content = json.loads(packet.content.decode("utf8"))
                yield packet

    def encode(self) -> bytes:
        assert self._short_tag != 2  # 2 means DEFLATE, do not send by client
        if self.packet_type == PacketType.POPULARITY:
            buffer = struct.pack(">i", self.content)
        else:
            buffer = self.content.encode("utf8")
        header_length = 16
        total_length = header_length + len(buffer)
        header = bytearray(struct.pack(">ihhii", total_length, header_length,
                                       self._short_tag, self.packet_type.value, self._tag))
        header.extend(buffer)
        return header

    async def send_to(self, ws: websockets.WebSocketClientProtocol):
        await ws.send(self.encode())
