# server script
The script you provided is a Python server script that sets up a server to handle client connections and perform certain tasks based on the received data. Let's break down the script's functionality:

It imports the necessary modules and libraries for socket communication, SSL/TLS encryption, file handling, logging, and threading.

## The find_path() function:
reads a configuration file (config.config) and retrieves the path to a file specified in the configuration.
It returns the obtained file path

## The handle_client() function
processes the data received from a client connected to the server.
It receives the client socket object, the file path, and a boolean value indicating whether the file should 
be reread on each query or not. It performs operations on the received data, checks if it exists in the specified
file, and sends a response back to the client.

## The start_server() function
is responsible for setting up the server. It takes the host address, port number, file path, reread flag, and an SSL 
configuration dictionary as parameters. It creates a socket object, binds it to the host and port,
and listens for incoming connections. If SSL is enabled, it creates an SSL context, loads the server-side certificate
and key, and wraps the socket with SSL/TLS encryption. It then enters a loop to accept client connections and submits
each client handling task to a thread pool executor for concurrent processing.

## The find_config_path() function
finds the path to the configuration file (config.ini) used by the server script.

## The server_config() function
reads the server configuration from the config.ini file. It retrieves the necessary values for host, port, reread flag,
and SSL configuration, and returns them in a dictionary.

Finally, in the main part of the script, the server configuration is obtained using server_config(). The file path is retrieved using find_path(). Logging is configured with a specific format and level. Then, the start_server() function is called with the obtained server configuration values and the file path to start the server.

To use this server script, you need to have the required configuration files (config.config and config.ini) properly set up, 
as well as the necessary dependencies installed.
The server will listen for incoming client connections, handle their requests based on the defined logic, and respond accordingly.

## Example on how to run the server.py script:
### python3 server.py

# client
This code is a client application that communicates with a server using SSL/TLS encryption.
It sends a query string to the server and receives a response indicating whether the string exists in the server's database.
The code also measures the execution time for different file sizes.

## prerequisite
To run this code, you need the following:

Python 3.x installed on your system.
The socket and ssl modules, which are standard libraries in Python.

## setup
Clone or download the code repository to your local machine.

Make sure you have the server module in the same directory as the client code.
The server module contains the server configuration needed for the client.

## running the code
Open a terminal or command prompt.

Navigate to the directory containing the client code.

Run the following command to execute the client code:
### python client.py --query "your_query_string"

Replace "your_query_string" with the string you want to search for in the server's database.

The code will establish a secure connection with the server, send the query string, and receive a response.
The response will be printed on the console as shown below assuming the query string is valid.

### Example: python client.py --query "19;0;21;16;0;17;3;0;"
![Screenshot](https://github.com/Mumin8/Server_script/blob/main/op.PNG)

## Understanding the Code
The search_string function is responsible for establishing a secure connection with the server, sending the query string, and receiving the response.

The code uses SSL/TLS encryption to ensure secure communication between the client and the server.

The server_config function retrieves the server configuration from the server module.

The code measures the execution time for different file sizes by repeating the search process for each size.


