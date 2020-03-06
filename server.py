import socket, sys, os

def main():
    # Create a TCP/IP socket
    # print(sys.argv[1])
    # sys.exit()
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (str(sys.argv[1]),20000)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connectionskey
    sock.listen(1)

    sock.setblocking(0)
    print('waiting for a connection')
    while True:
        try:
            connection, client_address = sock.accept()
            print('connection from', client_address)
                    # Receive the data in small chunks and retransmit it in uppercase
            data = connection.recv(2000)
            data = data.decode("utf-8")
            if data:
                print('received "%s"' % data)
            print('waiting for a connection')
        except BlockingIOError:
            pass

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main()
    except KeyboardInterrupt:
        try:
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)