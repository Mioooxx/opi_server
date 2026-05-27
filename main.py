#!/usr/bin/env python

import asyncio
import serial, json
from websockets.asyncio.server import serve

arduino_port = "/dev/ttyUSB0"
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

async def hello(websocket):
    async for name in websocket:
        print(f"<<< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f">>> {greeting}")

async def handleMsg(websocket):
    async for msg in websocket:
        print(f"<<< {msg}")
        command = json.loads(msg)
        type = command["type"]
        data = command["data"]
        timestamp = command["timestamp"]
        print(f"<<< {type} << {data} << {timestamp}")
        arduino_command = type + " " + data + "\n"
        ser.write(arduino_command.encode())

async def main():
    async with serve(handleMsg, "0.0.0.0", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())