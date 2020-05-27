import enum
import time

BASE_DOMAIN = "bilibili.com"

API_PROTOCOL = "https"
API_SUB_DOMAIN = "api.live"
API_PREFIX = f"{API_PROTOCOL}://{API_SUB_DOMAIN}.{BASE_DOMAIN}"

DANMAKU_PROTOCOL = "wss"
DANMAKU_SUB_DOMAIN = "broadcastlv.chat"
DANMAKU_DOMAIN = f"{DANMAKU_SUB_DOMAIN}.{BASE_DOMAIN}"
DANMAKU_PORT = 443
DANMAKU_PATH = "/sub"
DANMAKU_FULL_URL = f"{DANMAKU_PROTOCOL}://{DANMAKU_DOMAIN}:{DANMAKU_PORT}{DANMAKU_PATH}"


@enum.unique
class API(enum.Enum):
    ROOM_INIT = "/room/v1/Room/mobileRoomInit"


BUILD_VERSION_ID = "XZEBD7DEB19AE02C8BDBB8B7919D7AAF02180"
DEVICE_ID = "KREhESMUJRMlEiVGOkY6QDgJblpoC3sRdQ"


def COMMON_HEADERS(init_time): return {
    "Display-ID": f"{BUILD_VERSION_ID}-{init_time}",
    "Buvid": BUILD_VERSION_ID,
    "User-Agent": "Mozilla/5.0 BiliDroid/5.39.0 (bbcallen@gmail.com)",
    "Device-ID": DEVICE_ID,
    "Accept-Encoding": "gzip",
}


def COMMON_QUERY(appkey): return {
    "actionKey": "appkey",
    "appkey": appkey,
    "build": "5390000",
    "device": "android",
    "mobi_app": "android",
    "platform": "android",
}
