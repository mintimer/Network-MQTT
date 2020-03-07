import socket, sys, os
from threading import Thread

def closeAllConnect (): # Closing socket connection from 'All Subscriber' by send message 
    for topic in portlist:
        for socket in portlist[topic]:
            # Query all in 'portlist' and send closing message
            socket['socket_connection'].send(b'BROKER_CLOSE_CONNECT')

def closeConnByAddr(client_address): # Closing socket connection from 'an Address' by delete socket from 'portlist'
    for topic in portlist:
        for i in range(len(portlist[topic])):
            # found address in 'portlist'
            if portlist[topic][i]['client_address'] == client_address: 
                # delete socket from 'portlist'
                print()
                print('Closing Connection from {}'.format(client_address) + ' topic "%s"' % topic)
                del portlist[topic][i]
                break

def closeConnByTopic(topic,socket_connection): # Closing socket connection from 'All Subsciber on specific topic' from 'Publisher'
    # check topic if not found, send response to Publisher
    if topic in portlist:
        # check Subscriber in topic if don't have, send response to Publisher
        if portlist[topic] == []:
            print('Not found subscriber on topic "%s"' % topic)
            socket_connection.send(b'404') # 404 not found
        else:
            # if found, send message to all Subscriber on this topic to close connection
            for anytopic in portlist:
                if anytopic == topic:
                    for i in range(len(portlist[topic])):
                        portlist[topic][i]['socket_connection'].send(b'PUBLISH_CLOSE_CONNECT')
                        print('Closing Connection by Publisher')
                        print('from {}'.format(portlist[topic][i]['client_address']) + ' topic "%s"' % topic)
            del portlist[topic] # and delete socket data from 'portlist'
            socket_connection.send(b'SUCCESS')
    else: 
        print('Not found subscriber on topic "%s"' % topic)
        socket_connection.send(b'404') # 404 not found
    

def publishData(topic,data,socket_connection): # publishing data message to all Subscriber
    # check topic if not found, send response to Publisher
    if topic in portlist:
        # check Subscriber in topic if don't have, send response to Publisher
        if portlist[topic] == []:
            print('Not found subscriber on topic "%s"' % topic)
            socket_connection.send(b'404') # 404 not found
        else:
            for anytopic in portlist:
                if anytopic == topic:
                    # if found, send data message to all Subcriber in topic
                    for socket in portlist[topic]:
                        socket['socket_connection'].send(data.encode())
                        print('send "' + data + '" to ' + topic + ' ' + str(socket['client_address']))
            socket_connection.send(b'SUCCESS')
    else: 
        print('Not found subscriber on topic "%s"' % topic)
        socket_connection.send(b'404') # 404 not found
    

def addSubscribe(topic,socket_connection,client_address): # add new Subscriber socket connection to 'portlist' 
    print('received from Subscriber topic "%s"' % topic)
    if topic in portlist: # if there is topic in portlist (not new topic in portlist)
        # add connection and address to list in that topic
        portlist[topic].append({'socket_connection':socket_connection , 'client_address':client_address }) 
    else : # add connection and address to list in new topic
        portlist[topic] = [{'socket_connection':socket_connection , 'client_address':client_address }]

def isSubcriber(message): # check message if it is from Subscriber return True
    return 'SUB\t' in message

def isPublisher(message): # check message if it is from Publisher return True
    return 'PUB\t' in message

def manage_connect(socket_connection, client_address): # Manage all connection from Subscriber or Publisher
    print()
    print('connection from', client_address)
    # loop waiting for connection receive
    while True:
        try:
            message = socket_connection.recv(2000)
            message = message.decode('utf-8')
            if message:
                if isSubcriber(message): # check is Subscriber
                    splited = str(message).split('\t') # split message from 'SUB\t[Message]'
                    topic = splited[1]
                    if topic == 'CLOSE_CONNECT': # check closing message
                        closeConnByAddr(client_address) # close connection from this subscriber
                        break
                    else :
                        addSubscribe(topic,socket_connection,client_address) # add socket and address of subscriber to topic list in 'portlist'
                if isPublisher(message): # check is Publisher
                    splited = str(message).split('\t') # split message from 'PUB\t[Message]'
                    topic = splited[1]
                    data = splited[2]
                    if data == 'CLOSE_CONNECT': # check closing message
                        closeConnByTopic(topic,socket_connection) # close connection of all subscriber with this topic from publisher
                    else:
                        publishData(topic,data,socket_connection) # send data message to all subscriber with this topic from publisher
        except BlockingIOError: # Do not care and do anything if don't have any receive to message (non-blocking proccess error)
            pass

def main():
    if len(sys.argv)==2: # check valid input argument
        server_address = (str(sys.argv[1]),20000)
        print('starting up on %s port %s' % server_address)
        try: # check server has been running or not
            sock.bind(server_address)
        except OSError:
            print('this broker server can not running or has been running.')
            try:
                sock.close()
                sys.exit(0)
            except:
                os._exit(0)
        # Listen for incoming connections key
        sock.listen(1)
        # set process to non-blocking (for waiting KeyboardInterrupt)
        sock.setblocking(0)
        # Loop for all socket accept
        while True:
            try:
                socket_connection, client_address = sock.accept()
                try: # threading 'manage_connect' for more connection in same process
                    Thread(target=manage_connect,args=(socket_connection,client_address)).start()
                except:
                    print("Cannot start thread..")
            except BlockingIOError: # Do not care and do anything if don't have any socket accept (non-blocking proccess error)
                pass
    else : # invalid input argument message
        print()
        print('Error! Please put valid Argument')
        print('ex : python broker.py [IP-ADDRESS]')
        print('ex : python broker.py 127.0.0.1')
        print()
        try: # close program
            sock.close()
            sys.exit(0) 
        except:
            os._exit(0)

# Close all connection and program when have KeyboardInterrupt 
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initial
        portlist = dict() # set 'portlist' to dictionary data structure to keep all data of socket connection from all subscriber 
        main()
    except KeyboardInterrupt:
        closeAllConnect() # close all socket connection
        print()
        print('sending connection closing message to all subscriber')
        print('closing Broker..')
        try: 
            sock.close() # close server socket
            sys.exit(0) # close program
        except:
            os._exit(0)