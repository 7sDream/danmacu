import json
import os
import sys

from .command import Danmaku, Gift
from .danmaku_client import DanmakuClient


class CommandLineOutputDanmakuClient(DanmakuClient):
    @classmethod
    def on_init_room(cls, result: bool, extra: str):
        print("init room:", "succ" if result else f"failed: {extra}")
        if result is False:
            return False  # do not retry

    @classmethod
    def on_enter_room(cls, result: bool, extra: object):
        print("enter room:", "succ" if result else "failed")

    @classmethod
    def on_danmaku(cls, danmaku: Danmaku):
        badge = f'[{danmaku.badge} {danmaku.badge_level}]' if danmaku.badge is not None else ''
        print(f'{badge}[UL {danmaku.level}]{danmaku.user}: {danmaku.message}')

    @classmethod
    def on_gift(cls, gift: Gift):
        print(f'{gift.user} 赠送了 {gift.name} x {gift.count}')

    @classmethod
    def on_error(cls, error):
        print("error:", error)

    @classmethod
    def on_close(cls, error):
        print("close", error)


def main():
    appkey = os.getenv("DANMACU_APPKEY")
    secret = os.getenv("DANMACU_SECRET")

    if appkey is None:
        appkey = ""

    if secret is None:
        secret = ""

    if len(sys.argv) < 2 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} <room_id>")
        exit(0)

    room_id = int(sys.argv[1])

    dc = CommandLineOutputDanmakuClient(appkey, secret, room_id)

    dc.start()


if __name__ == "__main__":
    main()
