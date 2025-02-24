# Credit Card MicroService
---
CS361, Winter 2025  
Written by: Michelle Mann  
Credit Card Microservice for Wei-Yin (Christine) Chen

## Starting the Server
---
Run the following command to start the server on port 5557 (as collectively decided by MM and WYC)
```sh
python3 cc_service.py
```

## Connect to the Server
---
To request data from the server, client programs can connect to the server via socket.connect per the example call below:
```python
context = zmp.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")
```

## Request Data from the Server
---
Requests can be made via the following format:  
Example request:
```sh
message = {"cc_number": "5100000000000008", "exp_date": "12/25"}
```
The microservice looks for two headers:
1. "cc_number"
2. "exp_date"

And all calls must be made with those headers.

Credit card numbers and expiration dates will be processed internally via the microservice and response messages will be appended to the original message. 

The request parameters in JSON can be sent to the microservice via socket.send_json() per the example call below:
```sh
socket.send_json(message_dict)
```

## Receive Data from the Server
---
All responses will be appended to the original message sent at the time of request. Example response:
```sh
{"cc_number": "4111111111111111", "exp_date": "01/99", "valid": true, "card_type": "Visa", "valid_exp": "Valid"}
{"cc_number": "5500000000000004", "exp_date": "05/2025", "valid": false, "error": "Invalid date format"}
{"cc_number": "2333 7777 7777 7779", "exp_date": "77/12", "valid": false, "error": "Invalid date format"}
```

**Note** - It should be noted that this microservice is functionally linear. If a test fails early (i.e. the header type is invalid), the microservice will close immediately after the failed test and will not continue to do further testing (i.e. test expiration date).

The response parameters in JSON can be received from the microservice via message = socket.recv() which will be returned via json.loads(message). For example:
```sh
message = socket()
print(f"The message sent back: {message.decode()}")
return json.loads(message)
```

## UML Diagram
---
![image](https://github.com/user-attachments/assets/48d80d26-3139-4896-a6ee-9021ef5aaebd)


