import socket ,sys ,os

def checkResponse(topic): # check response from broker that can send message to subscriber or not
    while True:
        try:
            response = sock.recv(2000) # waiting for response message
            response = response.decode('utf-8')
            if response == 'SUCCESS':
                print('Sending Success')
                break
            else :
                print('Not found subscriber on topic "%s"' % topic)
                break
        except BlockingIOError: # Do not care and do anything if don't have any recieve (non-blocking proccess error)
            pass

def main():
    if len(sys.argv)>=4: # check valid input argument
        server_address = (sys.argv[1], 20000)
        print('connecting to %s port %s' % server_address)
        # check connection if can not, close program
        try:
            sock.connect(server_address)
        except:
            print('Connection failed to {}'.format(server_address))
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        topic = sys.argv[2]
        message = sys.argv[3]
        # loop merge all message after message's whitespace to one string
        for i in range(len(sys.argv)-4):
            message = message + ' ' + sys.argv[i+4]
        # Send data
        print('sending "' + message + '" to ' + topic)
        message = 'PUB\t' + topic + '\t' + message # add Publisher prefix and splitable data by tab ('\t')
        try:
            sock.send(message.encode())
        except:
            print('Can not send message to broker')
            try: # close program
                sock.close()
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        # set process to non-blocking (for waiting KeyboardInterrupt)
        sock.setblocking(0)
        # check reponse message
        checkResponse(topic) 
    else: # invalid input argument message
        print()
        print('Error! Please put valid Argument')
        print('ex : python publisher.py [IP-ADDRESS] [Topic] [Message]')
        print('ex : python publisher.py 127.0.0.1 Room1 Hello Guys I love your cats')
        print('Note : Can\'t use whitespace in [Topic]')
        print('     : Can use whitespace in [Message]')
        print()
        try: # close program
            sys.exit(0)
        except:
            os._exit(0)

# Close program when have KeyboardInterrupt 
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initial
        main()
    except KeyboardInterrupt:
        try:
            print('closing socket')
            sock.close() # close socket
            sys.exit(0) # close program
        except:
            os._exit(0)