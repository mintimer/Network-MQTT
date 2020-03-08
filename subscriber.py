import socket ,sys ,os

def main():
    if len(sys.argv)==3: # check valid input argument
        server_address = (sys.argv[1], 20000)
        print('connecting to %s port %s' % server_address)
        # check connection if can not, close program
        try:
            sock.connect(server_address)
        except :
            print('Connection failed to {}'.format(server_address))
            try:
                sys.exit(0)
            except:
                os._exit(0)

        topic = sys.argv[2]
        print('Subscribing topic "%s"' % topic)
        message = 'SUB\t' + topic # add Subscriber prefix
        # try sending
        try:
            sock.send(message.encode())
        except :
            print('Can not send message to broker')
            try: # close program
                sock.close()
                sys.exit(0)
            except:
                os._exit(0)
        # set process to non-blocking (for waiting KeyboardInterrupt)
        sock.setblocking(0)
        while True:
            try:
                data = sock.recv(2000)
                if data:
                    data = data.decode('utf-8')
                    
                    # Broker is closed this socket
                    if('BROKER_CLOSE_CONNECT' == data):
                        sock.close() # close socket
                        print('subscriber connection closed by broker')
                        break
                    # Publisher is closed this socket
                    elif('PUBLISH_CLOSE_CONNECT' == data):
                        sock.close() # close socket
                        print('subscriber connection closed by publisher')
                        break

                    # Publisher published the message
                    else:
                        print("PUB : "+data)
                        
            except BlockingIOError:  # Do not care and do anything if don't have any receive (non-blocking proccess error)
                pass
    else : # invalid input argument message
        print()
        print('Error! Please put valid Argument')
        print('ex : python subscriber.py [IP-ADDRESS] [Topic]')
        print('ex : python subscriber.py 127.0.0.1 Room_1')
        print('Note : Can\'t use whitespace in [Topic]')
        print()
        try: # close program
            sys.exit(0)
        except:
            os._exit(0)
            
# Close all connection and program when have KeyboardInterrupt 
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main()
    except KeyboardInterrupt:
        sock.send(b'SUB\tCLOSE_CONNECT') # send closing connection message to broker
        print('subscriber connection closed')
        try:
            sock.close() # close socket
            sys.exit(0) # close program
        except:
            os._exit(0)