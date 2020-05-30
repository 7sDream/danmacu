import asyncio
import functools
import json
import os
import sys

import websockets

from .command import Danmaku, Gift
from .danmaku_client import DanmakuClient
from .debug import CommandLineOutputDanmakuClient
from .server import DanmakuClientAsWebsocketServer


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

    kls = None
    if len(sys.argv) >= 3 and sys.argv[2] == '--debug':
        kls = CommandLineOutputDanmakuClient
    else:
        kls = functools.partial(
            DanmakuClientAsWebsocketServer, "127.0.0.1", 5678)

    dc = kls(appkey, secret, room_id)
    asyncio.get_event_loop().run_until_complete(dc.start())

    # do not stop
    print("stop")


if __name__ == "__main__":
    main()
