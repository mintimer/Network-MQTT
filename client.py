import socket ,sys ,os

def main():
    # Connect the socket to the port where the server is listening
    server_address = (sys.argv[1], 20000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    message = sys.argv[2]

    try:
        # Send data
        print('sending "%s"' % message)
        sock.sendall(message.encode())

    finally:
        print('closing socket')
        sock.close()

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