import asyncio

async def task(name,delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)#delay work
    print(f"Task {name} finished after {delay} sec")

async def main():
    #schedule tasks to run concurrently
    task1=asyncio.create_task(task("A",2))
    task2=asyncio.create_task(task("B",1))

    await task1 #wait for task1 to finish
    await task2 #wait for task2 to finish

asyncio.run(main())    