import json
import time

CoolDowns = {}


async def update_data(users, user):
    if not f"{user.id}" in users:
        users[f"{user.id}"] = {}
        users[f"{user.id}"]["experience"] = 0
        users[f"{user.id}"]["level"] = 1


async def add_experience(users, user, exp):
    global CoolDowns
    try:
        CoolDowns.update({user.id: f"{user.id}:{CoolDowns[user.id][user.id]}"})
    except:
        CoolDowns.update({user.id: f"{0}"})
    print(float(CoolDowns[user.id]) - int(time.time()) <= 60)
    print(print(float(CoolDowns[user.id]) - int(time.time())))
    if (float(CoolDowns[user.id]) - float(time.time())) <= 60:
        users[f"{user.id}"]["experience"] += exp
        CoolDowns.update({user.id: f"{time.time()}"})
        print("added xp")


async def level_up(users, user, message):
    with open("levels.json", "r") as g:
        levels = json.load(g)
    experience = users[f"{user.id}"]["experience"]
    lvl_start = users[f"{user.id}"]["level"]
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f"{user.mention} has leveled up to level {lvl_end}")
        users[f"{user.id}"]["level"] = lvl_end


async def setLvl(users, user, lvl):
    users[f"{user.id}"]["experience"] = 0
    users[f"{user.id}"]["level"] = lvl
