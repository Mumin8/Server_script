import socket


HOST = '127.0.0.1'
port = 8000 


def search_string(query):
    '''
    search_string: it is a client for the server application

    args:
        query: the query string for the search
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:

        soc.connect((HOST, port))
        soc.send(query.encode())
        res = soc.recv(1024).decode()
        print(res)
        if res == 'string found':
            print(res)
        else:
            print(res)


search_string('3;0;1;28;0;7;5;0;')
