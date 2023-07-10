import socket
import ssl
import time
import argparse
from server import server_config


def search_string(query_string: str) -> str:
    '''
    search_string: it is a client for the server application

    args:
        query_string: the query string for the search
    '''

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((HOST, PORT)) as soc:
            with context.wrap_socket(soc, server_hostname=HOST) as secure_soc:
                secure_soc.send(query_string.encode())
                res = secure_soc.recv(1024).decode()
                if res == 'STRING EXISTS':
                    print(f'{res}')
                    return res
                else:
                    print(f'{res}')
                    return res

    except socket.error as e:
        print(f'{e}')
    except ssl.SSLError as e:
        print(f"SSL error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    except socket.error as e:
        print(f'{e}')
    except ssl.SSLError as e:
        print(f"SSL error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


'''
file_sizes = [10000, 50000, 100000, 500000, 1000000]


for size in file_sizes:
    query = query_string * (size // 16)
    start_time = time.time()
    search_string(query)
    end_time = time.time()
    execution_time = end_time - start_time
    print()
    print()
    print(f'File size: {size}')
    print(f"Execution time: {execution_time} seconds")
'''
if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="Query string")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the query string
    query = args.query

    # Get the server configuration
    server = server_config()
    HOST = server["host"]
    PORT = server["port"]

    # Perform the search
    search_string(query)
