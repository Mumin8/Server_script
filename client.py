import socket
import ssl
import time

HOST = '127.0.0.1'
PORT = 8000


def search_string(query: str) -> str:

    '''
    search_string: it is a client for the server application

    args:
        query: the query string for the search
    '''

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((HOST, PORT)) as soc:
            with context.wrap_socket(soc, server_hostname=HOST) as secure_soc:
                secure_soc.send(query.encode())
                res = secure_soc.recv(1024).decode()
                if res == 'STRING EXISTS':
                    return res
                else:
                    return res

    except socket.error as e:
        print(f'{e}')
    except ssl.SSLError as e:
        print(f"SSL error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


search_string('3;0;1;28;0;7;5;0;')

'''
file_sizes = [10000, 50000, 100000, 500000, 1000000]


for size in file_sizes:
    query = '17;0;1;26;0;19;5;0;' * (size // 16)
    start_time = time.time()
    search_string(query)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"File size: {size} | Execution time: {execution_time} seconds")
    '''
