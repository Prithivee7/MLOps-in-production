import asyncio
import json
import aiohttp

async def do_post(session, url, x):
    async with session.post(url, data = json.dumps(x),headers={"Content-Type": "application/json"}) as response:
        data = await response.text()
        return data

async def main_func():
    url = '<Enter the AKS url here>'
    resp_ls = [ {"Pclass": 3, "Sex": 1, "Age": 34.5, "SibSp":0,"Parch":0,"Fare":7.8292,"Embarked":2},
                {"Pclass": 3, "Sex": 0, "Age": 40, "SibSp":1,"Parch":1,"Fare":2.56,"Embarked":0},
                {"Pclass": 3, "Sex": 0, "Age": 12, "SibSp":1,"Parch":2,"Fare":300,"Embarked":1},
                {"Pclass": 3, "Sex": 1, "Age": 18, "SibSp":1,"Parch":5,"Fare":4.1,"Embarked":0},
                {"Pclass": 3, "Sex": 0, "Age": 71, "SibSp":0,"Parch":1,"Fare":72,"Embarked":1},
                {"Pclass": 3, "Sex": 1, "Age": 26, "SibSp":0,"Parch":0,"Fare":1.8,"Embarked":2}
            ]
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        for req in resp_ls:
            post_tasks.append(do_post(session, url, req))
        # now execute them all at once
        val = await asyncio.gather(*post_tasks)
        return val

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
val = asyncio.run(main_func())
failed_request_count = 0 
for resp in val:
    try:
        d = json.loads(resp)
        print(d)
    except:
        failed_request_count += 1

print("Number of requests sent",len(val))
print("Number of requests failed",failed_request_count)