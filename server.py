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

    while True:
        try:
            # Wait for a connection
            # print('waiting for a connection')
            connection, client_address = sock.accept()
            print('connection from', client_address)
                    # Receive the data in small chunks and retransmit it in uppercase
            while True:
                data = connection.recv(2000)
                if(len(data) > 0):
                    print('received "%s"' % data.decode('utf-8'))
                    if data:
                        print('sending data in uppercase back to the client')
                        data = data.decode('utf-8').upper().encode()
                        connection.sendall(data)
                    else:
                        print('no more data from', client_address)
                        break
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