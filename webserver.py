from socket import *
import sys  # For terminating the program

serverSocket = socket(AF_INET, SOCK_STREAM) #tells the socket connection to use ipv4 (our ip adress or localhost) and 2nd attribute
                                            #tells the socket to use TCP connection (SOCK_DGRAM is UDP)

# Prepare a server socket
serverPort = 4305  # port number

serverSocket.bind(('localhost', serverPort)) #localhost is me, bind command binds the local host to run server port, so its "localhost:[port number]"

serverSocket.listen(1)  # Listen for incoming connections (opens up the connection to allow users to connect to it) and the attribute limits it to 1 user request (others will be rejected)

print(f'Server is ready and listening on port {serverPort}...') #signifies code ran and server should be running

while True:  #infinite loop

    # Establish the connection
    connectionSocket, addr = serverSocket.accept() #sets up the port and ip adress for this connection (client) and accepts the connection

    print('Ready to serve...')  #flags the server has started

    try:

        message = connectionSocket.recv(1024).decode() #decodes 1kb of data recieved from "localhost[port num]"
        
        print(message) #displays the message, being the socket id


        #closes connection if the connection socket is not what is expected (null value or empty string, meaning it is True for this condition to close the connection)
        if not message:
            connectionSocket.close()
            continue


        filename = message.split()[1] #message variable has lots of info, so we split it to only show document we are searching for
        f = open(filename[1:], 'r')  # Open the requested file
        outputdata = f.read() #file we looked for is being read and stored to outputdata
        f.close() #closes file after we are done with it
        
        # Send HTTP response header
        responseHeader = "HTTP/1.1 200 OK\r\n\r\n" #code 200 ok being sent
        connectionSocket.send(responseHeader.encode()) #encodes the data to send. This is two steps in 1
        
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)): #checks the length of the file and loops the code below to the corresponding length
            connectionSocket.send(outputdata[i].encode()) #send line by line data encoded to the page
        
        """connectionSocket.send("\r\n".encode()) #not too sure why chatgpt wrote this but it sends a new blank line and moves the cursor to the 2nd last line"""
        connectionSocket.close() #closes connection after we are done

    except IOError:
        # Send response message for file not found (runs when the code under try function fails)
        responseHeader = "HTTP/1.1 404 Not Found\r\n\r\n" #error msg
        responseBody = "<html><head></head><body><h1>404 Not Found</h1></body></html>" #writing html code with python
        connectionSocket.send(responseHeader.encode()) #sending the encoded version of the string variables (same for below)
        connectionSocket.send(responseBody.encode())
        
        # Close client socket
        connectionSocket.close() #closes connection after we are done

#closes the server socket if it was not already closed
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
