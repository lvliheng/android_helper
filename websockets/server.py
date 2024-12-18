import asyncio
import websockets

def start():
  global connections
  connections = set()
  
  asyncio.run(main())
  
async def main():
  async with websockets.serve(echo, "192.168.0.2", 8765):
    await asyncio.Future()

async def echo(websocket):
  global connections
  if websocket not in connections:
    connections.add(websocket)
    
  async for message in websocket:
    print("echo: message:", message)
    websockets.broadcast(connections, message)

if __name__=="__main__":
  start()