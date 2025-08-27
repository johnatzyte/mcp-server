import asyncio
from fastmcp import Client

client = Client("main.py")

async def call_httpbin():
    async with client:
        result = await client.call_tool("httpbin")
        print(result)


async def extract_data(url: str):
    async with client:
        result = await client.call_tool("extract_html", {"url": url})
        print(result)

#asyncio.run(call_httpbin())
asyncio.run(extract_data("https://www.keychron.uk/products/keychron-k2-wireless-mechanical-keyboard-uk-iso-layout?variant=41479113605290"))