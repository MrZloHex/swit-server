import json
import asyncio
import websockets

class SwimShit:
    port = 5431
    is_ready = False 
    buffer = ""

    def __init__(self, port):
        self.port = port

    async def update(self):
        async with websockets.connect('ws://127.0.0.1:8000') as websocket:
            boot_msg = { "method": "state", "value": "swit"}
            await websocket.send(json.dumps(boot_msg))
            response = await websocket.recv()
            print(response)
            while True:
                response = await websocket.recv()
                print(response)



def main():
    swimshit = SwimShit(8800)
    asyncio.get_event_loop().run_until_complete(swimshit.update())


if __name__ == "__main__":
    main()