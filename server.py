import socket, json, time, uuid
from datetime import datetime, timezone

HOST = "0.0.0.0"   # listen on all interfaces
PORT = 5000        # port for RPC


def add(a, b): return a + b
def multiply(a, b): return a * b
def echo(message): return message

METHODS = {"add": add, "multiply": multiply, "echo": echo}


def log(msg):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
log(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    try:
        data = conn.recv(4096).decode()
        if not data:
            conn.close()
            continue

  
        try:
            request = json.loads(data)
        except json.JSONDecodeError:
            response = {"request_id": "N/A", "status": "ERROR", "error": "Invalid JSON"}
            conn.send(json.dumps(response).encode())
            conn.close()
            continue

        req_id = request.get("request_id", str(uuid.uuid4()))
        method = request.get("method")
        params = request.get("params", {})

        log(f"Received request_id={req_id}, method={method}, params={params}")

        # --- Simulate delay for failure demo ---
        # time.sleep(5)

        
        if method in METHODS:
            try:
                result = METHODS[method](**params)
                response = {"request_id": req_id, "status": "OK", "result": result}
            except Exception as e:
                response = {"request_id": req_id, "status": "ERROR", "error": str(e)}
        else:
            response = {"request_id": req_id, "status": "ERROR", "error": f"Unknown method {method}"}

        
        conn.send(json.dumps(response).encode())

    finally:
        conn.close()