#!/usr/bin/env python3
"""Test hosted-write-stream API endpoint"""
import asyncio
import httpx

async def test_hosted_write():
    url = "http://localhost:8007/api/v1/novels/novel-1775066530753/hosted-write-stream"
    payload = {
        "from_chapter": 6,
        "to_chapter": 10,
        "auto_save": True,
        "auto_outline": True
    }

    print(f"Testing: POST {url}")
    print(f"Payload: {payload}\n")

    async with httpx.AsyncClient(timeout=300.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}\n")

            if response.status_code != 200:
                text = await response.aread()
                print(f"Error: {text.decode()}")
                return

            print("Streaming events:\n")
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    print(line)

if __name__ == "__main__":
    asyncio.run(test_hosted_write())
