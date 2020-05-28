import hashlib
import time
from typing import Dict
from urllib.parse import quote

import requests

from .values import API, API_PREFIX, COMMON_HEADERS, COMMON_QUERY


class RoomInfo:
    def __init__(self, data: Dict[str, any]):
        self.room_id = data["data"]["room_id"]
        self.user_id = data["data"]["uid"]


class APICallException(Exception):
    pass


class APIClient:
    def __init__(self, appkey: str, secret: str):
        self._appkey = appkey
        self._secret = secret
        self._init_time = round(time.time())

    def __sign(self, query: Dict[str, str]) -> str:
        message = sorted(
            [f'{quote(k)}={quote(v)}' for k, v in query.items()]).join("&")
        return hashlib.md5(f'{message}{self._secret}'.encode('utf8'))

    @staticmethod
    def __api_url(path: str) -> str:
        return f'{API_PREFIX}{path}'

    def __call_api(self, path: str, query: Dict[str, str], headers: Dict[str, str] = None) -> Dict[str, any]:
        if headers is None:
            headers = {}
        return requests.get(self.__api_url(path), query, headers=dict(**COMMON_HEADERS(self._init_time), **headers)).json()

    def init_room(self, room_id: int) -> [int, int]:
        query = dict(
            id=str(room_id),
            ts=str(round(time.time())),
            **COMMON_QUERY(self._appkey),
        )
        query["sign"] = self.__sign(query)
        res = self.__call_api(API.ROOM_INIT.value, query)
        if res["code"] != 0:
            raise APICallException(res["message"])
        return RoomInfo(res)
