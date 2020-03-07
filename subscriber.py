import socket ,sys ,os

def main():
    if len(sys.argv)==3:
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
                    
                    # Broker is closed this socket
                    if('BROKER_CLOSE_CONNECT' == data):
                        sock.close()
                        print('subscriber connection closed by broker')
                        break
                    # Publisher is closed this socket
                    elif('PUBLISH_CLOSE_CONNECT' == data):
                        sock.close()
                        print('subscriber connection closed by publisher')
                        break

                    # Publisher published the message
                    else:
                        print("PUB : "+data)
                        
            except BlockingIOError:
                pass
            except:
                import traceback
                traceback.print_exc()
    else :
        print()
        print('Error! Please put valid Argument')
        print('ex : python subscriber.py [IP-ADDRESS] [Topic]')
        print('ex : python subscriber.py 127.0.0.1 Room_1')
        print('Note : Can\'t use whitespace in [Topic]')
        print()
        try:
            sys.exit(0)
        except:
            os._exit(0)
            
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main()
    except KeyboardInterrupt:
        sock.send(b'SUB\tCLOSE_CONNECT')
        print('subscriber connection closed')
        try:
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)