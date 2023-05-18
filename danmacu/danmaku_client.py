import abc
import asyncio
import enum
import json
import ssl
import threading
import time
import traceback
from functools import partial
from typing import Type

import websockets

from .api_client import APIClient, RoomInfo
from .command import CommandType, Danmaku, Gift, InteractWord
from .packet import Packet, PacketType
from .values import DANMAKU_FULL_URL


class DanmakuWebsocketClient:
    def __init__(self, room: RoomInfo):
        self._room = room

    @staticmethod
    async def _heartbeat(ws: websockets.WebSocketClientProtocol):
        while True:
            await asyncio.sleep(15)
            await Packet.HeartBeat().send_to(ws)

    @staticmethod
    async def __worker(client: "DanmakuClient", room: RoomInfo):
        async with websockets.connect(DANMAKU_FULL_URL) as ws:
            await Packet.EnterRoom(room).send_to(ws)
            # do not await, let it run in backend
            heart_beat_task = asyncio.create_task(
                DanmakuWebsocketClient._heartbeat(ws))

            while True:
                try:
                    message = await ws.recv()
                    for packet in Packet.parse(message):
                        try:
                            if packet.packet_type == PacketType.ENTER_ROOM_RESPONSE:
                                result = packet.content["code"] == 0
                                if await client.on_enter_room(result, packet.content) is False:
                                    ws.close()
                                    return
                            elif packet.packet_type == PacketType.COMMAND:
                                await client._on_ws_command_callback(packet.content)
                            elif packet.packet_type == PacketType.POPULARITY:
                                await client.on_popularity(packet.content)
                                #print("other packet_content = {}".format(packet.content))
                        except:
                            traceback.print_exc()
                            pass
                except websockets.ConnectionClosed as e:
                    heart_beat_task.cancel()
                    await client.on_close(e)
                    break
                except Exception as e:
                    await client.on_error(e)

    async def start(self, client: "DanmakuClient"):
        await DanmakuWebsocketClient.__worker(client, self._room)


class DanmakuClient(abc.ABC):
    def __init__(self, appkey: str, secret: str, room_id: int):
        self._appkey = appkey
        self._secret = secret
        self._room_id = room_id
        self._user_id = None

    async def __worker(self, appkey: str, secret: str, room_id: str):
        api = APIClient(appkey, secret)

        while True:
            try:
                room = api.init_room(room_id)
                break
            except Exception as e:
                if await self.on_init_room(False, e) is False:
                    return

        await self.on_init_room(True, room)

        ws = DanmakuWebsocketClient(room)

        await ws.start(self)

    async def start(self):
        await self.__worker(self._appkey, self._secret, self._room_id)

    async def _on_ws_command_callback(self, command: object):
        cmd = command["cmd"]
        print(command)
        if cmd == CommandType.DANMAKU.value:
            await self.on_danmaku(Danmaku(command["info"]))
        elif cmd == CommandType.GIFT.value:
            await self.on_gift(Gift(command["data"]))
        elif cmd == CommandType.INTERACTWORD.value:
            await self.on_interact_word(InteractWord(command['data']))
        else:
            pass
        # # If you want see other commands, uncomment bellow
        # else:
        #     print(json.dumps(command, ensure_ascii=False))

    @abc.abstractmethod
    async def on_init_room(self, result: bool, extra: str):
        pass

    @abc.abstractmethod
    async def on_enter_room(self, result: bool, extra: object):
        pass

    @abc.abstractmethod
    async def on_popularity(self, content: object):
        pass

    @abc.abstractmethod
    async def on_danmaku(self, danmaku: object):
        pass

    @abc.abstractmethod
    async def on_gift(self, gift: object):
        pass

    @abc.abstractmethod
    async def on_interact_word(self, InteractWord: object):
        pass

    @abc.abstractmethod
    async def on_error(self, error):
        pass

    @abc.abstractmethod
    async def on_close(self, error):
        pass
