import socket ,sys ,os

def main():
    # Connect the socket to the port where the server is listening
    server_address = (sys.argv[1], 20000)
    print('connecting to %s port %s' % server_address)
    
    try:
        sock.connect(server_address)
    except ConnectionRefusedError:
        print('Connection failed to {}'.format(server_address))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    message = sys.argv[2]
    print('Subscribing topic "%s"' % message)
    message = 'SUB\t' + message
    sock.send(message.encode())
    sock.setblocking(0)
    while True:
        try:
            data = sock.recv(2000)
            if(len(data) > 0):
                data = data.decode('utf-8')
                
                # Broker is closed or publisher wants to disconnect this socket
                if('CLOSE_CONNECT' == data):
                    sock.close()
                    print('Subscriber Connection Closed by Broker')
                    break

                # Publisher published the message
                else:
                    print("PUB : "+data)
                    
        except BlockingIOError:
            pass
        except:
            import traceback
            traceback.print_exc()
            
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main()
    except KeyboardInterrupt:
        sock.send(b'SUB\tEND_CONNECT')
        print('Subscriber Connection Closed')
        try:
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)