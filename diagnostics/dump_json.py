#!/usr/bin/python3

"""Nexia Climate Device Access"""
import sys

sys.path.insert(0, ".")


import argparse
import code
import readline
import rlcompleter
import time

import asyncio
import aiohttp

from nexiaux360.home import NexiaHome


async def _runner(username, password, brand):
    session = aiohttp.ClientSession()
    try:
        nexia_home = NexiaHome(
            session, username=username, password=password, brand=brand
        )
        await nexia_home.login()
        await nexia_home.update()
    finally:
        await session.close()
    return nexia_home


parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_const", const=True, help="Enable debug.")
parser.add_argument("--brand", type=str, help="Brand (nexia or asair or trane).")
parser.add_argument("--username", type=str, help="Your username/email address.")
parser.add_argument("--password", type=str, help="Your password.")
args = parser.parse_args()
brand = args.brand or BRAND_NEXIA


if args.username and args.password:
    nexia_home = asyncio.run(_runner(args.username, args.password, brand))
else:
    parser.print_help()
    exit()

print(nexia_home.devices_json)
print(nexia_home.automations_json)
