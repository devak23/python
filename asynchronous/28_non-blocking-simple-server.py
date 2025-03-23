# Operating systems have efficient APIs that let us watch sockets for incoming data and other events built in. While
# the actual API is dependent on the operating system (kqueue, epoll, and IOCP are a few common ones), all of these
# I/O notification systems operate on a similar concept. We give them a list of sockets we want to monitor for
# events, and instead of constantly checking each socket to see if it has data, the operating system tells us
# explicitly when sockets have data.

# Because this is implemented at the hardware level, very little CPU utilization is used during this monitoring,
# allowing for efficient resource usage. These notification systems are the core of how asyncio achieves concurrency.
# Understanding how this works gives us a view of how the underlying machinery of asyncio works.

# The event notification systems are different depending on the operating system. Luckily, Python’s selectors module
# is abstracted such that we can get the proper event for wherever we run our code. This makes our code portable
# across different operating systems.

# This library exposes an abstract base class called BaseSelector, which has multiple implementations for each event
# notification system. It also contains a DefaultSelector class, which automatically chooses which implementation is
# most efficient for our system.

# The BaseSelector class has important concepts. The first is registration. When we have a socket that we’re
# interested in getting notifications about, we register it with the selector and tell it which events we’re
# interested in. These are events such as read and write. Inversely, we can also deregister a socket we’re no longer
# interested in.

# The second major concept is select. select will block until an event has happened, and once it does, the call will
# return with a list of sockets that are ready for processing along with the event that triggered it. It also
# supports a timeout, which will return an empty set of events after a specified amount of time.

# Given all this, once we create our server socket, we’ll register it with the default selector, which will listen
# for any connections from clients. Then, any time someone connects to our server socket, we’ll register the client’s
# connection socket with the selector to watch for any data sent. If we get any data from a socket that isn’t our
# server socket, we know it is from a client that has sent data. We then receive that data and write it back to the
# client.

import socket
import selectors
from selectors import SelectorKey
from typing import List, Tuple
from asynchronous import logger

selector = selectors.DefaultSelector()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)
server_address = ('localhost', 8000)
server_socket.bind(server_address)
server_socket.listen(1)

selector.register(server_socket, selectors.EVENT_READ, data=None)

try:
    while True:
        try:
            events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

            if not events:
                logger.info("No events, waiting a bit more!")

            for event, _ in events:
                event_socket = event.fileobj

                if event_socket == server_socket:
                    try:
                        connection, address = server_socket.accept()
                        connection.setblocking(False)
                        logger.info(f"Connection obtained from {address}")
                        selector.register(connection, selectors.EVENT_READ, data=None)
                    except Exception as e:
                        logger.error(f"Error accepting connection: {e}")
                else:
                    try:
                        data = event_socket.recv(1024)
                        if data == b'':
                            logger.info("Client has disconnected")
                            selector.unregister(event_socket)
                            event_socket.close()
                            continue
                        else:
                            logger.info(f"I got some data: {data}")
                            event_socket.send(data)
                    except Exception as e:
                        logger.error(f"Error handing client: {e}")
                        selector.unregister(event_socket)
                        event_socket.close()
        except Exception as e:
            logger.error(f"Error in selector: {e}")
except KeyboardInterrupt as ke:
    logger.info("Shutting down server")
    selector.close()
    server_socket.close()
