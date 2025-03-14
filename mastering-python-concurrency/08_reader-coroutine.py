import asyncio

SERVER_PORT = 4444

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"message = {message}")
    writer.write(f"Echo: {message}".encode())
    await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', SERVER_PORT)
    async with server:
        print(f"server started. Listening on {SERVER_PORT}")
        await server.serve_forever()



if __name__ == '__main__':
    asyncio.run(main())

# In this example, the event loop schedules coroutines that manage network I/O operations. The function handle_client
# is executed for every new connection, and by awaiting I/O operations, it ensures that control is returned to the event
# loop during blocking operations.

# Event-driven programming also introduces a change in the error-handling model. Since tasks are decoupled and
# scheduled by the event loop, exceptions thrown within a coroutine must be captured and handled carefully. The
# event loop often provides mechanisms such as exception handlers or callbacks that can be registered to manage
# errors.