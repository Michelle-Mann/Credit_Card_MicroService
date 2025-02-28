"""This is a python program demonstrating ZeroMQ
Written by: Michelle Mann

This is the client side of the socket and should send the message
"This is a message from CS361"
"""

import zmq
import json
import time


def send_reqest_test(request_data):

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
    socket.send_string(request_data)

    # Step #7: Get the reply.
    message = socket.recv()
    print(f"Server sent back: {message.decode()}")

    return json.loads(message)


# Creation of our credit card data.
cc_nums = ["4111111111111111", "5500000000000004", "5199111111111113",
           "5199111111111118", "2333 7777 7777 7779", "3400-0000-0000-009",
           "1234567891234563"]
exp_dates = ["01/99", "05/2025", "5/27", "12/28", "77/12", "8-25", "10/30"]

test_cases = ["Valid Visa / Expired Date", "Valid MC / Bad Date Format",
              "Valid MC / Valid Date", "Valid MC, Bad Checksum",
              "Valid MC / Bad Date Format", "Valid AmEx / Bad Date Format",
              "Invalid Header"]


# Coverts the JSON message to string.
for i in range(len(cc_nums)):
    credit_card_data = {
        "cc_number": cc_nums[i],
        "exp_date": exp_dates[i],
        }

    print(test_cases[i])

    json_message = json.dumps(credit_card_data)
    send_reqest_test(json_message)
    time.sleep(1)

# Send quit signal after all tests are done
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")
socket.send_string("Q")
socket.close()
context.term()

print("All tests completed. Quit signal sent.")
