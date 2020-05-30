import enum
import json


@enum.unique
class CommandType(enum.Enum):
    DANMAKU = "DANMU_MSG"
    GIFT = "SEND_GIFT"


class Command:
    def __init__(self, cmd: CommandType):
        self.cmd = cmd.value

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


class Danmaku(Command):
    def __init__(self, obj: object):
        super().__init__(CommandType.DANMAKU)
        self.user = obj[2][1]
        self.message = obj[1]
        self.level = obj[4][0]
        self.level_color = obj[4][2]
        if len(obj[3]) > 0:
            self.badge = obj[3][1]
            self.badge_level = obj[3][0]
            self.badge_color = obj[3][4]
        else:
            self.badge = None
            self.badge_level = None


class Gift(Command):
    def __init__(self, obj: object):
        super().__init__(CommandType.GIFT)
        self.user = obj["uname"]
        self.name = obj["giftName"]
        self.count = obj["num"]
