import socket, json, uuid, time
from datetime import datetime, timezone

SERVER_IP = "your-private-ip"
PORT = 5000

def log(msg):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")

def send_request(method, params, retries=3, timeout=2):
    request = {
        "request_id": str(uuid.uuid4()),
        "method": method,
        "params": params
    }

    for attempt in range(1, retries+1):
        try:
            log(f"Attempt {attempt}/{retries} → sending {request}")
            s = socket.socket()
            s.settimeout(timeout)
            s.connect((SERVER_IP, PORT))
            s.send(json.dumps(request).encode())

            reply = s.recv(4096).decode()
            s.close()

            log(f"Received reply: {reply}")
            return json.loads(reply)

        except socket.timeout:
            log("Timeout waiting for response — retrying...")
        except Exception as e:
            log(f"Connection error: {e}")
            time.sleep(0.5)

    return {"request_id": request["request_id"], "status": "FAILED", "error": "No response after retries"}

# --- Example calls ---
print("RPC add:", send_request("add", {"a": 5, "b": 7}))
print("RPC multiply:", send_request("multiply", {"a": 3, "b": 4}))
print("RPC echo:", send_request("echo", {"message": "hello from client"}))