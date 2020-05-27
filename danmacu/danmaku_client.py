import abc
import enum
import ssl
import threading
import traceback
from functools import partial
from typing import Type

import websocket

from .api_client import APIClient, RoomInfo
from .packet import Packet, PacketType
from .values import DANMAKU_FULL_URL


class DanmakuWebsocketClient:
    def __init__(self, room: RoomInfo):
        self._room = room

    @staticmethod
    def on_open(room: RoomInfo, ws: websocket.WebSocket):
        Packet.EnterRoom(room).send_to(ws)

    @staticmethod
    def on_message(enter_callback, command_callback, ws: websocket.WebSocket, message):
        for packet in Packet.parse(message):
            try:
                if packet.packet_type == PacketType.ENTER_ROOM_RESPONSE:
                    result = packet.content["code"] == 0
                    if enter_callback(result, packet.content) is False:
                        ws.close()
                        return
                elif packet.packet_type == PacketType.COMMAND:
                    command_callback(packet.content)
            except:
                # TODO: traceback.print_exc()
                pass

    @staticmethod
    def on_error(callback, ws, error):
        callback(error)

    @staticmethod
    def on_close(callback, ws):
        callback()

    @staticmethod
    def __worker(cls: Type['DanmakuClient'], room: RoomInfo) -> bool:
        return websocket.WebSocketApp(
            DANMAKU_FULL_URL,
            on_open=partial(DanmakuWebsocketClient.on_open, room),
            on_message=partial(DanmakuWebsocketClient.on_message,
                               cls.on_enter_room,
                               cls._on_ws_command_callback),
            on_error=partial(DanmakuWebsocketClient.on_error, cls.on_error),
            on_close=partial(DanmakuWebsocketClient.on_close, cls.on_close),
        ).run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def start(self, cls: Type['DanmakuClient']) -> threading.Thread:
        worker = threading.Thread(target=DanmakuWebsocketClient.__worker, kwargs={
            "cls": cls, "room": self._room
        })
        worker.start()
        return worker


class DanmakuClient(abc.ABC):
    def __init__(self, appkey: str, secret: str, room_id: int):
        self._appkey = appkey
        self._secret = secret
        self._room_id = room_id
        self._user_id = None

    @classmethod
    def __worker(cls, appkey: str, secret: str, room_id: str):
        api = APIClient(appkey, secret)

        while True:
            try:
                room = api.init_room(room_id)
                break
            except Exception as e:
                if cls.on_init_room(False, e) is False:
                    return

        cls.on_init_room(True, room)

        ws = DanmakuWebsocketClient(room)

        ws_thread = ws.start(cls)

        ws_thread.join()

    def start(self):
        self.__worker(self._appkey, self._secret, self._room_id)

    @classmethod
    def _on_ws_command_callback(cls, command: object):
        cls.on_danmaku(command)

    @abc.abstractclassmethod
    def on_init_room(cls, result: bool, extra: str):
        pass

    @abc.abstractclassmethod
    def on_enter_room(cls, result: bool, extra: object):
        pass

    @abc.abstractclassmethod
    def on_danmaku(cls, danmaku: object):
        pass

    @abc.abstractclassmethod
    def on_gift(cls, gift: object):
        pass

    @abc.abstractclassmethod
    def on_error(cls, error):
        pass

    @abc.abstractclassmethod
    def on_close(cls, error):
        pass
