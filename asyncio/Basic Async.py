import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # Simulate a delay (non-blocking)
    print("World!")

async def main():
    await say_hello()  # Runs sequentially

asyncio.run(main())  # Starts the event loop