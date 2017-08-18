"""https://www.reddit.com/r/python/top.json

https://www.reddit.com/r/emacs/top.json"""

import asyncio
import json
import signal
import sys

import aiohttp


loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)

URL_TEMPLATE = \
    "https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5"


async def get_json(subreddit, client):
    url = URL_TEMPLATE.format(subreddit=subreddit)
    with aiohttp.Timeout(10):
        async with client.get(url) as response:
            assert response.status == 200
            return await response.read()


async def get_reddit_top(subreddit, client):
    response = await get_json(subreddit, client)
    data = json.loads(response.decode('utf-8'))
    for item in data['data']['children']:
        score = item['data']['score']
        title = item['data']['title']
        link = item['data']['url']
        print(str(score) + ': ' + title + ' (' + link + ')')

    print('DONE: {}'.format(subreddit))


def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

asyncio.ensure_future(get_reddit_top('python', client))
asyncio.ensure_future(get_reddit_top('programming', client))
asyncio.ensure_future(get_reddit_top('compsci', client))
loop.run_forever()
