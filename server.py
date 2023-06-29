#!/usr/bin/env python

from configparser import ConfigParser
import socket
import threading


def find_path() -> str:
    '''
    find_path: the function to find the path to the file


    Return:
            the path to the file
    '''

    with open('config.config', 'r') as conf_file:
        for line in conf_file:
            if line.startswith('linuxpath='):
                file_path = line
                print(f' this is the path {file_path}')
                break
            else:
                ValueError('path not in configuration file')
    return file_path


def handle_client(
        client_socket: object, file_path: str, reread_on_query: bool):
    '''
    handle_client:
        it handles the client clear text string

    args:
        client_socket: the object of the client socket

        file_path:
            the path to the file to read from

        reread_on_query:
            the boolean to determine whether on not to read from the file again
    '''

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # decode the received string from the client and strip null characters
        the_string = data.decode('utf-8').strip('\x00')

        if reread_on_query:
            # checks whether the query string is in the file and read ones
            with open(file_path.lstrip('linuxpath=/').rstrip('\n'),
                      'r') as file:

                if the_string in file.read():
                    resp = "STRING EXISTS\n"
                else:
                    resp = "STRING DOES NOT EXIST\n"
        else:
            # goes through the file to look for a match
            with open(file_path.lstrip('linuxpath=/').rstrip('\n'),
                      'r') as file:

                for line in file:
                    if line.strip() == the_string:
                        resp = "STRING EXISTS\n"
                        break
                else:
                    resp = 'STRING DOES NOT EXIST\n'

        client_socket.send(resp.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def start_server(host: str, port: int, file_path: str, reread_on_query: bool):
    '''
    start_server: binds a port and responds to unlimited amount of
    concurrent connections

    args:
        host:
            a string representing the host or ip address of the server
        port:
            an integer representing the port number of the server to bind
        file_path:
                the path to the file to read from
        reread_on_query:
                boolean to check whether to reread a file or not
        '''

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host} : {port}")

    while True:
        # Accept a client connection
        client_sock, client_addr = server_socket.accept()
        print(f"New connection from {client_addr[0]} : {client_addr[1]}")

        # Start a new thread to handle the client
        client_th = threading.Thread(
                    target=handle_client,
                    args=(client_sock, file_path, reread_on_query))

        # start the thread
        client_th.start()


if __name__ == '__main__':
    # Specify the host and port to bind the server to
    HOST = '127.0.0.1'
    PORT = 8000

    REREAD_ON_QUERY = True

    # Start the server
    file_path = find_path()

    start_server(HOST, PORT, file_path, REREAD_ON_QUERY)
