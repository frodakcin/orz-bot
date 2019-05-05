import json
from discord import Embed

POTD_DATA_FILE_PATH = 'potd.json'
CONTENDER_LIST = []
MAX_POINTS = 1000000


class Contender:
    def __init__(self, user, name, pts):
        self.user = user
        self.username = name
        self.points = pts

    def __lt__(self, other):
        if self.points != other.points:
            return self.points < other.points
        return False

    def __gt__(self, other):
        if self.points != other.points:
            return self.points > other.points
        return False

    def update_points(self, gained):
        new_points = min(self.points + gained, MAX_POINTS)
        if new_points < 0:
            new_points = 0
        self.points = new_points

    def to_JSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True, indent=4
        )


def update_contender(x):
    if isinstance(x, Contender):
        for i in range(len(CONTENDER_LIST)):
            if CONTENDER_LIST[i].user == x.user:
                x.update_points(CONTENDER_LIST[i].points)
                del CONTENDER_LIST[i]
                break
        A = True
        for i in range(len(CONTENDER_LIST)):
            if x > CONTENDER_LIST[i]:
                CONTENDER_LIST.insert(i, x)
                A = False
                break
        if A:
            CONTENDER_LIST.append(x)
        save()


async def getContenderList(bot, message):
    e = Embed(title='POTD Leaderboard')
    for i in range(10):
        try:
            e.add_field(name=f'str(i+1). {CONTENDER_LIST[i].username}',
                        value=f'{CONTENDER_LIST[i].points} points',
                        inline=False)
        except:
            break
    await bot.send_message(message.channel, embed=e)


async def getContenderData(bot, message):
    name = message.mentions[0].id
    for i in CONTENDER_LIST:
        if i.user == Contender(name, name, 0).user:
            await bot.send_message(
                message.channel,
                f'{i.username} has {i.points} points for POTD',
            )


async def updateLeaderboard(bot, message):
    try:
        name = message.mentions[0].id
        nameToShow = message.mentions[0].display_name
        try:
            content = message.content[:message.content.index('pts')].strip()
        except:
            content = message.content.strip()
        score = min(int(content.split()[-1]), MAX_POINTS)
        if score < 0:
            score = 0
        update_contender(Contender(name, nameToShow, score))
    except:
        pass

# START IO


def encode_contender(x):
    if isinstance(x, Contender):
        return {'user': (x.user), 'username': (x.username), 'pts': (x.points)}
    else:
        raise TypeError(
            'Object of type {dt.__class__.__name__} is not compatible with encode_contender')


def decode_contender(x):
    return Contender(x['user'], x['username'], x['pts'])


def save():
    with open(POTD_DATA_FILE_PATH, 'w') as write_file:
        json.dump(CONTENDER_LIST, write_file,
                  default=encode_contender, sort_keys=False, indent=2)


def load():
    global CONTENDER_LIST
    with open(POTD_DATA_FILE_PATH, 'r') as read_file:
        CONTENDER_LIST = json.load(read_file, object_hook=decode_contender)
# END IO
