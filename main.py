import os
import requests
from nextcord.ext import commands
from typing import Union

serverdata = {"guild_id": -1}

bot = commands.Bot(
    command_prefix=os.__doc__
)  # command_prefix=os.__doc__ -> command_prefix 안 쓴다는 뜻


def rolename_and_id(query: Union[str, int]) -> Union[str, int]:
    """
    :param query: str이 들어오면 이름을 검색해서 UID 리턴, int가 들어오면 id를 검색해서 이름 리턴
    :return: 유노
    """
    url = f"https://discord.com/api/guilds/{serverdata['guild_id']}/roles"
    head = {"Authorization": f"Bot {os.environ['token']}"}
    r = requests.get(url, headers=head)

    for i in r.json():

        if type(query) == int:  # query==int
            if query == i["id"]:
                return i["name"]
        else:  # query==str
            if query == i["name"]:
                return int(i["id"])


def get_rolename():
    """
    :return:권한들 순서대로 정렬해서 리턴, 0이 최상위
    """
    url = f"https://discord.com/api/guilds/{serverdata['guild_id']}/roles"
    head = {"Authorization": f"Bot {os.environ['token']}"}
    r = requests.get(url, headers=head)

    unsorted = {}  # 미정렬된 무지성 리스트들

    for i in r.json():
        unsorted[i["position"]] = i["name"]

    res = []  # 정렬된 리스트

    for i in sorted(unsorted, reverse=True):
        res.append(unsorted[len(unsorted) - i - 1])  # 키만 들어있는 리스트->값만 들어있는 리스트
    return res


def generate_main_role_to_permission(main_role: list) -> list:
    """
    :param main_role:주된 권한 몇 개 받으면 서브권한 리스트 뽑아서 돌려주기
    :return: 위에서 가져온 리스트
    """
    permmap = {}  # todo 이거 완성


@bot.event
async def on_member_update(before, after):
    # nextcord.member.Member -> list with uid
    before_permlist = before.roles
    before_perm = []
    for i in before_permlist:
        before_perm.append(i.id)

    after_permlist = after.roles
    after_perm = []
    for i in after_permlist:
        after_perm.append(i.id)

    del after_permlist  # clean debug watch list
    del before_permlist
    # todo generate_main_role_to_permission이랑 섞어서 권한 부여
    print(before_perm, after_perm)  # 이건 BreakPoint 찍으려고 넣은 의미없는 코드


def run():
    if os.environ["debug"] == "1":
        serverdata["guild_id"] = 919974679559688232  # 스테이징 길드ID
    else:
        serverdata["guild_id"] = 868429217740783637  # 자매앱 길드ID
    bot.run(os.environ["token"])
