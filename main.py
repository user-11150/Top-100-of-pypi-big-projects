import aiohttp
import asyncio
import json
import os
import time

async def main():
    async with aiohttp.request(method="GET", url="https://pypi.org/stats", headers={"Accept": "application/json"}) as request:
        content = await request.content.read()
        content_str = content.decode()
        content = json.loads(content_str)
        top = content["top_packages"]
        with open("README.md", mode="wt") as f:
            header = f"""\
PyPI 上最大的项目TOP100

更新时间：{time.strftime("%B %Y, %d %H:%M:%S")}
"""
            f.write(header)
            for idx, package in enumerate(sorted(top, key=lambda item: top[item]["size"]), start=1):
                print(f"{idx}. [{package} {top[package]['size'] / 1024 / 1024}MB](https://pypi.org/project/{package})", file=f)
        os.system(
            "git add .;"
            "git commit -m \"Update\";"
            "git push"
        )

if __name__ == "__main__":
    asyncio.run(main())
