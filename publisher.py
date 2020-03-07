import socket ,sys ,os

def main():
    # Connect the socket to the port where the server is listening
    server_address = (sys.argv[1], 20000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    topic = sys.argv[2]
    message = sys.argv[3]

    try:
        # Send data
        print('sending ' + message + ' to ' + topic)
        message = 'PUB\t' + topic + '\t' + message
        sock.send(message.encode())

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