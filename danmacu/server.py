import asyncio
import importlib
import logging
import os

import aiohttp.web
import websockets

from .command import Danmaku, Gift, InteractWord, Popularity
from .danmaku_client import DanmakuClient


class LocalHTTPServer():
    def __init__(self, ip: str, port: int):
        static = os.path.dirname(
            importlib.util.find_spec("danmacu.static").origin)

        self._ip = ip
        self._port = port

        app = aiohttp.web.Application()
        router = aiohttp.web.RouteTableDef()
        router.static("/", static)
        app.add_routes(router)
        self._app = app

    async def start(self):
        await asyncio.get_event_loop().create_server(self._app.make_handler(), self._ip, self._port)


class LocalDanmakuWebsocketServer(DanmakuClient):
    def __init__(self, ip: str, port: int, appkey: str, secret: str, room_id: int):
        super().__init__(appkey, secret, room_id)
        self._ip = ip
        self.clients = set()
        self._port = port
        self._server: websockets.Serve = None

    async def listen(self):
        self._server: websockets.Serve = websockets.serve(
            self._new_client, host=self._ip, port=self._port)
        await self._server

    async def start(self):
        await asyncio.gather(super().start(), self.listen())

    async def message_all(self, message):
        for ws in self.clients:
            await ws.send(message)

    async def _new_client(self, ws: websockets.WebSocketServerProtocol, path: str):
        print("New Client Enter")
        if path == "/" and ws not in self.clients:
            self.clients.add(ws)
            await ws.wait_closed()
            print("Client leave")
            self.clients.remove(ws)
        else:
            await ws.close()

    async def on_init_room(self, result: bool, extra: str):
        pass

    async def on_enter_room(self, result: bool, extra: object):
        pass

    async def on_popularity(self, content: object):
        await self.message_all(Popularity(content[0]).to_json())
        print(content)
        print("人气 = {}".format(content[0]))

    async def on_danmaku(self, danmaku: Danmaku):
        await self.message_all(danmaku.to_json())
        print(danmaku.to_json())

    async def on_gift(self, gift: Gift):
        await self.message_all(gift.to_json())

    async def on_interact_word(self, interact_word: InteractWord):
        await self.message_all(interact_word.to_json())

    async def on_error(self, error):
        print(error)

    async def on_close(self, error):
        for ws in self.clients:
            await ws.close()
