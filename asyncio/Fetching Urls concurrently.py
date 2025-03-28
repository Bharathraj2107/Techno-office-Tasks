import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:#The with are used so that it will be cleared 
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls=[
        "https://example.com",
        "https://python.org",
        "https://github.com"
    ]  
    pages=await asyncio.gather(*[fetch_url(url) for url in urls])

    for url,content in zip(urls,pages):
        print(f"Fetched {url} (length:{len(content)})")
asyncio.run(main())              