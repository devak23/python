import tornado.ioloop
import tornado.web
import asyncio
import random

class AsyncHandler(tornado.web.RequestHandler):
    async def get(self):
        # Simulate an IO operation
        result = await self.execute_async_task()
        self.write(f"result = {result}")


    async def execute_async_task(self):
        # Wrap an asyncio.sleep call to simulate delay
        await asyncio.sleep(random.randint(1,10))
        return "Data processed successfully"


def make_app():
    return tornado.web.Application([
        (r"/", AsyncHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
