import socket

from asynchronous import logger

# We first use the socket function to create a socket. Here, we specify two parameters to the socket function. The
# first is socket.AF_INET—this tells us what type of address our socket will be able to interact with; in this case a
# hostname and a port number. The second is socket.SOCK_STREAM; this means that we use the TCP protocol for our
# communication. TCP, or transmission control protocol, is a protocol designed to transfer data between applications
# over a network. This protocol is designed with reliability in mind. It performs error checking, delivers data in
# order, and can retransmit data when needed. This reliability comes at the cost of some overhead. The vast majority
# of the web is built on TCP. TCP is in contrast to UDP, or user datagram protocol, which is less reliable but has
# much less overhead than TCP and tends to be more performant.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The following line will allow us to reuse the port number after we stop and restart the application, avoiding any
# address already in use errors. If we didn’t do this, it might take some time for the operating system to unbind
# this port and have our application start without error.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Calling socket.socket lets us create a socket, but we can’t start communicating with it yet because we haven’t
# bound it to an address that clients can talk to (our post office needs an address!). For this example, we’ll bind
# the socket to an address on our own computer at 127.0.0.1, and we’ll pick an arbitrary port number of 8000.
server_address = ('localhost', 8000)
server_socket.bind(server_address)
server_socket.listen(1)

logger.info(f"Echo server listening on {server_address}")
connection, client_address = server_socket.accept()
logger.info(f"Connection from {client_address}")

# OUTPUT
# 2025-03-22 12:06:09,092 - [INFO] - [27-simple-server.<module>]:~  Connection from ('127.0.0.1', 53708)

# Now that we’ve created a server capable of accepting connections. To read data from our connections, the socket
# class has a method named recv that we can use. This method takes an integer representing the number of bytes we
# wish to read at a given time. This is important because we can’t read all data from a socket at once; we need to
# buffer until we reach the end of the input. we’ll treat the end of input as a carriage return plus a line feed or
# '\r\n'. This is what gets appended to the input when a user presses the Enter key. We’ll set a buffer size
# intentionally low to see how buffering works. In a real-world application, we would use a larger buffer size,
# such as 1024 bytes as this will take advantage of the buffering that occurs at the operating system-level, which is
# more efficient than doing it in your application

buffer = b''
data = b''
BUFFER_SIZE = 1024  # bytes
try:
    while buffer[-2:] != b'\r\n':
        data = connection.recv(BUFFER_SIZE)
        if not data:
            break
        else:
            logger.info(f"I got {data}")
            buffer += data

    connection.sendall(b"server: " + data)
finally:
    connection.close()

# OUTPUT

# 2025-03-22 12:39:31,306 - [INFO] - [27-simple-server.<module>]:~  Connection from ('127.0.0.1', 37976)
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b'This is '
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b'a very l'
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b'ong sent'
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b'ence tha'
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b't I expe'
# 2025-03-22 12:39:36,743 - [INFO] - [27-simple-server.<module>]:~  I got b'ct the s'
# 2025-03-22 12:39:36,744 - [INFO] - [27-simple-server.<module>]:~  I got b'erver to'
# 2025-03-22 12:39:36,744 - [INFO] - [27-simple-server.<module>]:~  I got b' send me'
# 2025-03-22 12:39:36,744 - [INFO] - [27-simple-server.<module>]:~  I got b' back\r\n'

# Due to the small buffer size, we try to receive two bytes and store it in our buffer. Then, we go into a loop,
# checking each iteration to see if our buffer ends in a carriage return and a line feed. If it does not, we get two
# more bytes and print out which bytes we received and append that to the buffer. There is a problem with this
# implementation - the second connection initated with this program doesn't get to see any echo's from the echo server
# but the first one does get the echo. his is due to the default blocking behavior of sockets. The methods accept and
# recv block until they receive data. This means that once the first client connects, we will block waiting for it to
# send its first echo message to us. This causes other clients to be stuck waiting for the next iteration of the
# loop, which won’t happen until the first client sends us data. The non-blocking version is found in
# 28_non-blocking-simple-server.py
