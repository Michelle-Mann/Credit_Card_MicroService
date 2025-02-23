# Credit Card MicroService
---
CS361 - Credit Card Microservice  
Written by: Michelle Mann  
CS361, Winter 2025  

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
(TBD)

## UML Diagram
---
(TBD)
