import asyncio

loop = asyncio.SelectorEventLoop()
asyncio.set_event_loop(loop)

f = open('myfile', 'r')


def callback():
    print("Ping")
    return
    data = f.read()
    print(data)


loop.add_reader(f, callback=callback)
loop.run_forever()

f.close()
