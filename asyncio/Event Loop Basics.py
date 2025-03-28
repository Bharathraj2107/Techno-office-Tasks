import asyncio
async def print_number():
    for i in range(1,6):
        print(i)
        await asyncio.sleep(0.5)

async def print_letters():
    for letter in ['a','b','c','d','e']:
        print(letter)
        await asyncio.sleep(0.3)

async def main():
    #run both the functions at a time 
    await asyncio.gather(
        print_number(),
        print_letters()
    )                
asyncio.run(main())    