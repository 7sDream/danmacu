import asyncio
import functools
import json
import os
import sys

import websockets

from .command import Danmaku, Gift
from .danmaku_client import DanmakuClient
from .debug import CommandLineOutputDanmakuClient
from .server import LocalDanmakuWebsocketServer, LocalHTTPServer


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

    debug = False
    if len(sys.argv) >= 3 and sys.argv[2] == "--debug":
        debug = True

    tasks = []

    if debug:
        client = CommandLineOutputDanmakuClient(appkey, secret, room_id)
        tasks.append(client.start())
    else:
        websocket_server = LocalDanmakuWebsocketServer(
            "127.0.0.1", 7778, appkey, secret, room_id)
        http_server = LocalHTTPServer("127.0.0.1", 7777)
        tasks.append(websocket_server.start())
        tasks.append(http_server.start())
        print("Danmaku page: http://127.0.0.1:7777/index.html")
        print("Press Command+C to stop...")

    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    main()
