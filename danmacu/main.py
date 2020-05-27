import json
import os
import sys

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
    def on_danmaku(cls, danmaku: object):
        print("danmaku:", json.dumps(danmaku, ensure_ascii=False))

    @classmethod
    def on_gift(cls, gift: object):
        print("gift:", json.dumps(gift, ensure_ascii=False))

    @classmethod
    def on_error(cls, error):
        print("error:", error)

    @classmethod
    def on_close(cls, error):
        print("close", error)


def main():
    appkey = os.getenv("DANMACU_APPKEY")
    secret = os.getenv("DANMACU_SECRET")

    if appkey is None or secret is None:
        print("Please set your DANMACU_APPKEY and DANMACU_APPKEY enviroment var")
        exit(1)

    if len(sys.argv) < 2 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(f"usage: {sys.argv[0]} <room_id>")
        exit(0)

    room_id = int(sys.argv[1])

    dc = CommandLineOutputDanmakuClient(appkey, secret, room_id)

    dc.start()


if __name__ == "__main__":
    main()
