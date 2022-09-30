import websockets
import json
import asyncio
from time import sleep

class Server:
    def __init__(self, port):
        self.port = port
        self.tasks = set()
        self.web_conn = False
        self.swt_conn = False
        self.send_res = False
        self.pool_x = 1000
        self.pool_y = 1000
        self.velocity = 50
        self.angle_velocity = 40
        self.radius = 30
        self.machine_x = 200
        self.machine_y = 200

    def next_turn(self, turn):
        if turn == "right":
            return "left"
        elif turn == "left":
            return "right"

    def calc_route(self):
        route = list()
        turn = "right"
        cols = int(self.pool_x / self.machine_x)
        route.append(("forward", int((((self.pool_y - self.radius) / self.velocity) * 1000))))
        for i in range(0, cols-1):
            route.append((turn, int((180 / self.angle_velocity) * 1000)))
            turn = self.next_turn(turn)
            route.append(("forward", int((((self.pool_y - (2*self.radius)) / self.velocity) * 1000))))

        return route

    async def handler(self, websocket, path):
        while True:
            listener_task = asyncio.ensure_future(websocket.recv())
            producer_task = asyncio.ensure_future(self.make_output())
            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)

            if listener_task in done:
                message = listener_task.result()
                print(message)
                await self.process_input(json.loads(message), websocket)
            else:
                listener_task.cancel()

            if producer_task in done:
                message = producer_task.result()
                if self.send_res:
                    await websocket.send(message)
                    self.send_res = False
            else:
                producer_task.cancel()

    async def process_input(self, msg, websocket):
        if msg["method"] == "state":
            if msg["value"] == "swit":
                self.swt = websocket
                self.swt_conn = True
                self.tasks.add("swit_conn")
                print("HELLO SWIT")
            elif msg["value"] == "webpage":
                self.web = websocket
                self.web_conn = self.swt_conn
                self.tasks.add("web_conn")
                print("HELLO WEB")
        elif msg["method"] == "move":
            await self.swt.send(json.dumps({"method": msg["value"], "value": (msg["time"] * 1000)}))
        elif msg["method"] == "stop":
            await self.swt.send(json.dumps({"method": "stop"}))
        elif msg["method"] == "pool_dimensions":
            self.pool_x = msg["length"]
            self.pool_y = msg["width"]
        elif msg["method"] == "velocity":
            self.velocity = msg["value"]
        elif msg["method"] == "machine_dimensions":
            self.machine_x = msg["length"]
            self.machine_y = msg["width"]
        elif msg["method"] == "start":
            await self.auto_mode()
        
    async def make_output(self):
        try:
            task = list(self.tasks)[0]
        except:
            return ""
        
        self.tasks.discard(task)

        if task == "swit_conn":
            await self.swt.send(json.dumps({"result":self.swt_conn}))
        elif task == "web_conn":
            await self.web.send(json.dumps({"result":self.web_conn}))

        return ""


    async def auto_mode(self):
        route = self.calc_route()
        print(route)
        for step in route:
            await self.swt.send(json.dumps({"method":step[0], "value": step[1]}))
            sleep(step[1] / 1000)

        await self.swt.send(json.dumps({"method": "stop"}))








 


def main():
    server = Server(25565)
    server = websockets.serve(server.handler, "localhost", server.port)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()