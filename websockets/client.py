import asyncio
from websockets.asyncio.client import connect

def start():
  asyncio.run(main())
  
async def main():
  async with connect("ws://192.168.0.2:8765") as websocket:
    await websocket.send("test")
    message = await websocket.recv()
    print(message)

if __name__=="__main__":
  start()