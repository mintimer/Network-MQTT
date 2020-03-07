import socket ,sys ,os

def checkResponse(topic):
    while True:
        response = sock.recv(2000)
        response = response.decode('utf-8')
        if response == 'SUCCESS':
            print('Sending Success')
            break
        else :
            print('Not found subscriber on topic "%s"' % topic)
            break

def main():
    if len(sys.argv)>=4:
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

        topic = sys.argv[2]
        message = sys.argv[3]
        for i in range(len(sys.argv)-4):
            message = message + ' ' + sys.argv[i+4]

        try:
            # Send data
            print('sending "' + message + '" to ' + topic)
            message = 'PUB\t' + topic + '\t' + message
            sock.send(message.encode())
        except BlockingIOError: 
            pass

        checkResponse(topic)
    else:
        print()
        print('Error! Please put valid Argument')
        print('ex : python publisher.py [IP-ADDRESS] [Topic] [Message]')
        print('ex : python publisher.py 127.0.0.1 Room1 Hello Guys I love your cats')
        print('Note : Can\'t use whitespace in [Topic]')
        print('     : Can use whitespace in [Message]')
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
        try:
            print('closing socket')
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)