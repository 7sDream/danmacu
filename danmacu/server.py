from .command import Danmaku, Gift
from .danmaku_client import DanmakuClient


class DanmakuClientAsWebsocketServer(DanmakuClient):
    def __init__(self, ip: str, port: int, appkey: str, secret: str, room_id: int):
        super().__init__(appkey, secret, room_id)
        self.addr = f'{ip}:{port}'

    def on_init_room(self, result: bool, extra: str):
        pass

    def on_enter_room(self, result: bool, extra: object):
        pass

    def on_danmaku(self, danmaku: Danmaku):
        pass

    def on_gift(self, gift: Gift):
        pass

    def on_error(self, error):
        pass

    def on_close(self, error):
        pass
