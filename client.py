import socket
import ssl

HOST = '127.0.0.1'
PORT = 8000


def search_string(query):
    '''
    search_string: it is a client for the server application

    args:
        query: the query string for the search
    '''

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((HOST, PORT)) as soc:
        with context.wrap_socket(soc, server_hostname=HOST) as secure_soc:
            secure_soc.send(query.encode())
            res = secure_soc.recv(1024).decode()
            if res == 'STRING EXISTS':
                print(res)
            else:
                print(res)


search_string('17;0;1;26;0;19;5;0;')
