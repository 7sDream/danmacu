import asyncio
import logging

import websockets

from .command import Danmaku, Gift
from .danmaku_client import DanmakuClient

logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class DanmakuClientAsWebsocketServer(DanmakuClient):
    def __init__(self, ip: str, port: int, appkey: str, secret: str, room_id: int):
        super().__init__(appkey, secret, room_id)
        self._ip = ip
        self._port = port
        self._ws: websockets.WebSocketServerProtocol = None
        self._server: websockets.Serve = None

    async def listen(self):
        self._server: websockets.Serve = websockets.serve(
            self._new_client, host=self._ip, port=self._port)
        await self._server

    async def start(self):
        await asyncio.gather(super().start(), self.listen())

    async def _new_client(self, ws: websockets.WebSocketServerProtocol, path: str):
        print("new client from", path)
        if path == '/' and self._ws is None:
            self._ws = ws
            await self._ws.wait_closed()
            self._ws = None
        else:
            ws.close()

    async def on_init_room(self, result: bool, extra: str):
        pass

    async def on_enter_room(self, result: bool, extra: object):
        pass

    async def on_danmaku(self, danmaku: Danmaku):
        badge = f'[{danmaku.badge} {danmaku.badge_level}]' if danmaku.badge is not None else ''
        message = f'{badge}[UL {danmaku.level}]{danmaku.user}: {danmaku.message}'
        if self._ws is not None:
            await self._ws.send(message)

    async def on_gift(self, gift: Gift):
        message = f'{gift.user} 赠送了 {gift.name} x {gift.count}'
        if self._ws is not None:
            await self._ws.send(message)

    async def on_error(self, error):
        print(error.message)

    async def on_close(self, error):
        if self._ws is not None:
            self._ws.close()
