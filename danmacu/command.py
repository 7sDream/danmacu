import enum


@enum.unique
class CommandType(enum.Enum):
    DANMAKU = "DANMU_MSG"
    GIFT = "SEND_GIFT"


class Danmaku:
    def __init__(self, obj: object):
        self._raw = obj
        self.user = obj[2][1]
        self.message = obj[1]
        self.level = obj[4][0]
        if len(obj[3]) > 0:
            self.badge = obj[3][1]
            self.badge_level = obj[3][0]
        else:
            self.badge = None
            self.badge_level = None


class Gift:
    def __init__(self, obj: object):
        self._raw = obj
        self.user = obj["uname"]
        self.name = obj["giftName"]
        self.count = obj["num"]
