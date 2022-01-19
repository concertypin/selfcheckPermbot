import os
import requests
import nextcord
from nextcord.ext import commands
from typing import Union

serverdata = {"guild_id": -1}

bot = commands.Bot(command_prefix="bash ")


def rolename_and_id(query: Union[str, int]) -> Union[str, int]:
    """
    :param query: str이 들어오면 이름을 검색해서 UID 리턴, int가 들어오면 id를 검색해서 이름 리턴
    :return: 유노
    """
    url = f"https://discord.com/api/guilds/{serverdata['guild_id']}/roles"
    head = {"Authorization": f"Bot {os.environ['token']}"}
    r = requests.get(url, headers=head)

    t = {}

    for i in r.json():
        t[i["position"]] = i["name"]

        if type(query) == int:
            if query == i["id"]:
                return i["name"]
        else:
            if query == i["name"]:
                return int(i["id"])


def get_rolename():
    url = f"https://discord.com/api/guilds/{serverdata['guild_id']}/roles"
    head = {"Authorization": f"Bot {os.environ['token']}"}
    r = requests.get(url, headers=head)

    unsorted = {}

    for i in r.json():
        unsorted[i["position"]] = i["name"]

    res = []

    for i in sorted(unsorted):
        res.append(unsorted[len(unsorted) - i - 1])
    return res


def generate_main_role_to_permission(main_role: list) -> list:
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
    print(before_perm, after_perm)


def run():
    if os.environ["debug"] == "1":
        serverdata["guild_id"] = 919974679559688232
    else:
        serverdata["guild_id"] = 868429217740783637
    bot.run(os.environ["token"])


serverdata["guild_id"] = 868429217740783637
print(get_rolename())
