import socket, sys, os
from threading import Thread

def closeAllConnect ():
    for topic in portlist:
        for socket in portlist[topic]:
            socket['socket_connection'].send(b'BROKER_CLOSE_CONNECT')

def closeConnByAddr(client_address):
    for topic in portlist:
        for i in range(len(portlist[topic])):
            if portlist[topic][i]['client_address'] == client_address:
                print('Closing Connection from {}'.format(client_address) + ' topic "%s"' % topic)
                del portlist[topic][i]
                break

def closeConnByTopic(topic,socket_connection):
    if topic in portlist:
        if portlist[topic] == []:
            print('Not found subscriber on topic "%s"' % topic)
            socket_connection.send(b'404')
        else:
            for anytopic in portlist:
                if anytopic == topic:
                    for i in range(len(portlist[topic])):
                        portlist[topic][i]['socket_connection'].send(b'PUBLISH_CLOSE_CONNECT')
                        print('Closing Connection by Publisher')
                        print('from {}'.format(portlist[topic][i]['client_address']) + ' topic "%s"' % topic)
                        del portlist[topic][i]
            socket_connection.send(b'SUCCESS')
    else: 
        print('Not found subscriber on topic "%s"' % topic)
        socket_connection.send(b'404')
    

def publishData(topic,data,socket_connection):
    if topic in portlist:
        if portlist[topic] == []:
            print('Not found subscriber on topic "%s"' % topic)
            socket_connection.send(b'404')
        else:
            for anytopic in portlist:
                if anytopic == topic:
                    for socket in portlist[topic]:
                        socket['socket_connection'].send(data.encode())
                        print('send "' + data + '" to ' + topic + ' ' + str(socket['client_address']))
            socket_connection.send(b'SUCCESS')
    else: 
        print('Not found subscriber on topic "%s"' % topic)
        socket_connection.send(b'404')
    

def addSubscribe(topic,socket_connection,client_address):
    print('received from Subscriber topic "%s"' % topic)
    if topic in portlist:
        portlist[topic].append({'socket_connection':socket_connection , 'client_address':client_address })
    else :
        portlist[topic] = [{'socket_connection':socket_connection , 'client_address':client_address }]

def isSubcriber(message):
    return 'SUB\t' in message

def isPublisher(message):
    return 'PUB\t' in message

def manage_connect(socket_connection, client_address):
    print(' ')
    print('connection from', client_address)
    while True:
        try:
            message = socket_connection.recv(2000)
            message = message.decode('utf-8')
            if message:
                if isSubcriber(message):
                    splited = str(message).split('\t')
                    topic = splited[1]
                    if topic == 'CLOSE_CONNECT':
                        closeConnByAddr(client_address)
                        break
                    else :
                        addSubscribe(topic,socket_connection,client_address)
                if isPublisher(message):
                    splited = str(message).split('\t')
                    topic = splited[1]
                    data = splited[2]
                    if data == 'CLOSE_CONNECT':
                        closeConnByTopic(topic,socket_connection)
                    else:
                        publishData(topic,data,socket_connection)
        except BlockingIOError:
            pass

def main():
    if len(sys.argv)==2:
        server_address = (str(sys.argv[1]),20000)
        print('starting up on %s port %s' % server_address)
        try:
            sock.bind(server_address)
        except OSError:
            print('this broker server can not running or has been running.')
            try:
                sys.exit(0)
            except:
                os._exit(0)
        # Listen for incoming connectionskey
        sock.listen(1)
        sock.setblocking(0)
        while True:
            try:
                socket_connection, client_address = sock.accept()
                try:
                    Thread(target=manage_connect,args=(socket_connection,client_address)).start()
                except:
                    print("Cannot start thread..")
            except BlockingIOError:
                pass
    else :
        print()
        print('Error! Please put valid Argument')
        print('ex : python broker.py [IP-ADDRESS]')
        print('ex : python broker.py 127.0.0.1')
        print()
        try:
            sys.exit(0)
        except:
            os._exit(0)

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portlist = dict()
        main()
    except KeyboardInterrupt:
        closeAllConnect()
        print('sending connect closing message to all client')
        try:
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)