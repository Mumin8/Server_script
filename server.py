#!/usr/bin/env python

import configparser
import os
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from logging import basicConfig, DEBUG, debug, info
from threading import Thread
from time import time


def find_path() -> str:
    '''
    find_path: the function to find the path to the file


    Return:
            the path to the file

    '''
    # configparser object
    config = configparser.ConfigParser()
    config.read('config.config')

    if 'DEFAULT' in config:
        if 'linuxpath' in config['DEFAULT']:
            # obtain the exact path from the configuration file
            file_path = config['DEFAULT']['linuxpath']
            return file_path
    raise ValueError('path not in configuration file')


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
    start = time()

    # log information
    debug(f"Requesting IP: {client_socket.getpeername()[0]}")
    debug(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # process the data from the client
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # decode the received string from the client and strip null characters
        the_string = data.decode('utf-8').strip('\x00')

        if reread_on_query:
            # checks whether the query string is in the file and read ones
            # file_content = read_file(file_path)
            with open(file_path.lstrip(
                    'linuxpath=/').rstrip('\n'), 'r') as file:
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

        # the search query log information
        debug(f"Search query: {the_string}")
        client_socket.send(resp.encode('utf-8'))

        # the execution time of the program
        execution_time = time() - start
        debug(f"Execution time: {execution_time*1000} miliseconds")

    # Close the client socket
    client_socket.close()


def start_server(host: str, port: int, file_path: str,
                 reread_on_query: bool, openssl: dict
                 ):
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

        openssl_dict:
                    the configuration file to configure the ssl

        '''

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if openssl['ssl']:
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # Load server-side certificate and key
        context.load_cert_chain(certfile=openssl['certfile'],
                                keyfile=openssl['keyfile'])

        # Wrap the socket with SSL/TLS
        server_socket = context.wrap_socket(server_socket, server_side=True)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    info(f"Server listening on {host} : {port}")

    # create threadpoolexecutor with 10 max_workers
    executor = ThreadPoolExecutor(max_workers=10)

    while True:
        # Accept a client connection
        client_sock, client_addr = server_socket.accept()
        info(f"New connection from {client_addr[0]} : {client_addr[1]}")

        # submit client handling task to the executor
        executor.submit(handle_client,
                        client_sock, file_path, reread_on_query)

        # Start a new thread to handle the client
        # client_th = Thread(
        # target=handle_client,
        # args=(client_sock, file_path, reread_on_query))

        # start the thread
        # client_th.start()


def find_config_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'config.ini')


def server_config() -> dict:
    '''
    server_config: the function to setup the configuration
                    of the server

    Return:
        returns a diction of the necessary configurations
    '''

    config_path = find_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    server_section = config['Server']
    ssl_section = config['SSL']
    reread_section = config['REREAD']
    server_config = {
            'host': server_section.get('host'),
            'port': server_section.getint('port'),
            'REREAD_ON_QUERY': reread_section.getboolean('REREAD_ON_QUERY'),
            'USE_SSL': {
                'ssl': ssl_section.getboolean('ssl_status'),
                'certfile': ssl_section.get('certfile'),
                'keyfile': ssl_section.get('keyfile')
                }

            }

    return server_config


if __name__ == '__main__':

    # Read the server configuration
    server = server_config()

    file_path = find_path()
    basicConfig(
            level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s'
            )
    # start the server
    start_server(server['host'], server['port'],
                 file_path, server['REREAD_ON_QUERY'], server['USE_SSL'])
