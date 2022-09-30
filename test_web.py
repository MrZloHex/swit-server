import json
import asyncio
import websockets
from time import sleep

class SwimShit:
    port = 5431
    is_ready = False 
    buffer = ""

    def __init__(self, port):
        self.port = port

    async def update(self):
        async with websockets.connect('ws://127.0.0.1:8000') as websocket:
            boot_msg = { "method": "state", "value": "webpage"}
            movef_msg = { "method": "move", "value": "forward", "time": 10}
            moveb_msg = { "method": "move", "value": "backward", "time": 9}
            movel_msg = { "method": "move", "value": "left", "time": 11}
            mover_msg = { "method": "move", "value": "right", "time": 8}
            stop_msg = { "method": "stop"}
            start_msg = { "method": "start"}
            is_conn = False
            while not is_conn:
                await websocket.send(json.dumps(boot_msg))
                response = json.loads(await websocket.recv())
                is_conn = response["result"]
                print(response)
            while True:
                await websocket.send(json.dumps(movef_msg))
                await websocket.send(json.dumps(moveb_msg))
                await websocket.send(json.dumps(movel_msg))
                await websocket.send(json.dumps(mover_msg))
                await websocket.send(json.dumps(stop_msg))
                await websocket.send(json.dumps(start_msg))
                sleep(60)
                await websocket.send(json.dumps(stop_msg))
                response = await websocket.recv()
                print(response)



def main():
    swimshit = SwimShit(8000)
    asyncio.get_event_loop().run_until_complete(swimshit.update())


if __name__ == "__main__":
    main()