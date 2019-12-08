#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:6437"
    async with websockets.connect(uri) as websocket:
        result = ws.recv()

asyncio.get_event_loop().run_until_complete(hello())