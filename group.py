import asyncio
import random
import aiohttp

async def gen():
    return random.randint(1,7000000)

async def group():
    while True:
        id = await gen()
        async with aiohttp.ClientSession() as session:
                async with session.get(f"https://groups.roblox.com/v1/groups/{id}") as resp:
                    req = await resp.json()
                    print(f'[GROUP ID]:{id} is currently checking the data')
                    try:
                        locked = req['isLocked']
                    except:
                        locked = False
                    try:
                        if req['owner'] is None and req['publicEntryAllowed'] is True and locked is False:
                            members = req["memberCount"]
                            try:
                                async with session.get(f"https://economy.roblox.com/v1/groups/{id}/currency") as data:
                                    robux = await data.json()['robux']
                                print(f"Found {id} | Members : {members} | Robux$$ : {robux}$")
                                file = open("Groups.txt","a").write(f"Found {id} | Members : {members} | Robux$$ : {robux}$ \n")
                                file.close()
                            except:
                                print(f"Found {id} | Members : {members} | Robux$$ : Private")
                                file = open("Groups.txt","a").write(f"Found {id} | Members : {members} | Robux$$ : Private \n")
                                file.close()
                        else:
                            print(f"[GROUP ID]:{id} is already taken")
                    except:
                        print("you are being rate limited")
 

async def main():
    tasks = []
    for i in range(100):
        tasks.append(asyncio.Task(group()))
    await asyncio.wait(tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
