"""This is a python program demonstrating ZeroMQ
Written by: Michelle Mann

This is the client side of the socket and should send the message
"This is a message from CS361"
"""

import zmq
import json
import time

# Step #1: Set up the environment to enable socket creation.
context = zmq.Context()

# Step #2: Connect to the server to send a message.
print("Client attempting to connect to server...")

# Step #3: Creation of a request socket.
socket = context.socket(zmq.REQ)

# Step #4: Specifies the host and port#
socket.connect("tcp://localhost:5557")

# Step #5: Prints a message to console that we are sending a request.
print("Sending a request...")

# Step #6: Uses send_string to send a mesasge.

# Creation of our credit card data.
cc_nums = ["4111111111111111", "5500000000000004", "5199111111111113",
           "5199111111111118", "2333 7777 7777 7779", "3400-0000-0000-009",
           "1234567891234563"]
exp_dates = ["01/99", "05/2025", "5/27", "12/28", "77/12", "8-25", "10/30"]

# Coverts the JSON message to string.
for i in range(len(cc_nums)):
    credit_card_data = {
        "cc_number": cc_nums[i],
        "exp_date": exp_dates[i],
        }

    json_message = json.dumps(credit_card_data)
    socket.send_string(json_message)

    # Step #7: Get the reply.
    message = socket.recv()
    time.sleep(1)

    # Prints response.
    print(f"Server sent back: {message.decode()}")

# Step #8: Ends server
socket.send_string("Q")     # (Q)uit will ask server to stop.