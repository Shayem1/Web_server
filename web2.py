import threading
from socket import *
from tkinter import *
import tkinter as tk
import customtkinter
from selenium import webdriver
import time
import sys


def close_server():
    global serverSocket
    try:
        serverSocket.close()
    except OSError:
        pass  # Ignore if already closed


def handle_client(connectionSocket, addr):
    global logged_request
    try:
        message = connectionSocket.recv(1024).decode()  # Receive the HTTP request
        if not message:
            connectionSocket.close()
            return  # No message, return

        # Print the request headers (only once)
        if not logged_request:
            print(f"Received request from {addr}:")
            print(message)
            redirect_output(f"Received request from {addr}:\n{message}\n")  # Log to textbox
            logged_request = True  # Prevent logging multiple times

        # Process the requested file
        filename = message.split()[1]
        try:
            with open(filename[1:], 'r') as f:
                outputdata = f.read()

            responseHeader = "HTTP/1.1 200 OK\r\n\r\n"
            connectionSocket.send(responseHeader.encode())

            for char in outputdata:
                connectionSocket.send(char.encode())  # Send file content

        except IOError:
            # Handle file not found
            responseHeader = "HTTP/1.1 404 Not Found\r\n\r\n"
            responseBody = "<html><head></head><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(responseHeader.encode())
            connectionSocket.send(responseBody.encode())

    except OSError as e:
        print(f"Error with client {addr}: {e}")
    finally:
        connectionSocket.close()  # Close connection after handling the client

# Server update function that accepts and handles multiple connections
def server_update():
    global serverSocket
    while switch_var.get() == "on":
        try:
            # Accept a new client connection
            connectionSocket, addr = serverSocket.accept()
            print(f"New connection from {addr}")

            # Start a new thread to handle the client
            threading.Thread(target=handle_client, args=(connectionSocket, addr), daemon=True).start()

        except Exception as e:
            print(f"Error accepting new connection: {e}")
            break

# Function to start the server
def start_server():
    global serverSocket, number_of_clients
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverPort = 4305  # Port number
    serverSocket.bind(('localhost', serverPort))
    serverSocket.listen(number_of_clients)  # Allow up to 5 clients to queue up

    print(f'Server is ready and listening on port {serverPort}...')
    # Start accepting and handling connections
    threading.Thread(target=server_update, daemon=True).start()


def switch_toggle():
    global switch, switch_var
    if switch_var.get() == "on":
        switch.configure(state="disabled", progress_color="green")  # Green when on
        GUI.after(2000, lambda: switch.configure(state="normal"))  # Re-enable after 2 sec
        start_server()  # Start the server
    else:
        switch.configure(progress_color="red", fg_color="red")  # Red when off
        close_server()  # Close the server


def redirect_output(text):
    textbox.configure(state=NORMAL)
    textbox.insert("end", text)  # Insert message to the end of the textbox
    textbox.yview("end")  # Auto-scroll to the latest message
    textbox.configure(state=DISABLED)

def update_time():
    current_time = time.strftime("%H:%M:%S")  # Get current time
    clock_label.configure(text=current_time)  # Update label
    GUI.after(1000, update_time)  # Call function again after 1 sec

def open_webpage():
    driver = webdriver.Chrome()
    driver.get("http://localhost:4305/sev.html")

def thread_offload():
    threading.Thread(target=open_webpage, daemon=True).start()


# GUI Setup
GUI = customtkinter.CTk()
GUI.title("Web Server")
GUI.geometry("400x500")
GUI.minsize(width=400, height=500)
GUI.maxsize(width=400, height=500)
customtkinter.set_appearance_mode("dark")
GUI.configure(fg_color="black")

# Create a variable to track switch state
switch_var = customtkinter.StringVar(value="off")
switch = customtkinter.CTkSwitch(GUI, text="Server Switch", command=switch_toggle, variable=switch_var, onvalue="on",
                                 offvalue="off", font=("Arial", 20), progress_color="red", fg_color="red", corner_radius=20, border_width=0)
switch.place(relx=0.83, rely=0.853, anchor=SE)

# Frame for terminal output
frame = customtkinter.CTkFrame(GUI, corner_radius=40, fg_color="black")
frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.7, anchor=N)

# Create the scrollable Textbox
textbox = customtkinter.CTkTextbox(frame, wrap="word", height=10, state=DISABLED)
textbox.pack(side="left", fill="both", expand=True)

# Clock label
clock_label = customtkinter.CTkLabel(GUI, text="", font=("Arial", 20))
clock_label.place(relx=0.15, rely=0.86, anchor=SW)
update_time()  # Start updating the time

#setting up number of connections
# List of values from 1 to 8
combo_values = [str(i) for i in range(1, 9)]
# Create the ComboBox widget with the values from 1 to 8
combo_box = customtkinter.CTkComboBox(GUI, values=combo_values, width=50)
combo_box.place(relx=0.84, rely=0.953, anchor=SE)
combo_box.set("1")  # Set the default number of connections to 1
number_of_clients = int(combo_box.get())

connections_label = customtkinter.CTkLabel(GUI, text = "Connections", font=("Arial", 20))
connections_label.place(relx=0.69, rely=0.953, anchor=SE)

#creating test button
open_button = customtkinter.CTkButton(GUI, text="Test", command= lambda: thread_offload(), font=("Arial", 20), fg_color="grey18", width=80,
                                    hover_color="green", corner_radius=20)
open_button.place(relx=0.15, rely=0.953, anchor=SW)

# flag variable to indicate if the request was already performed
logged_request = False

# Redirect sys.stdout to the textbox
sys.stdout.write = redirect_output


GUI.mainloop()
