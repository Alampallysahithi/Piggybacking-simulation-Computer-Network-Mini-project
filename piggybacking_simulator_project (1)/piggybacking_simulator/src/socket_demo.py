import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 50505

def _server(result):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            data = conn.recv(4096)
            result.append(data.decode())
            conn.sendall(b"ACK: message received")

def send_demo_message(message):
    result = []
    thread = threading.Thread(target=_server, args=(result,), daemon=True)
    thread.start()
    time.sleep(0.05)
    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall(message.encode())
            ack = s.recv(4096).decode()
        thread.join(timeout=1)
        return f"TCP payload sent: '{message}' | Server response: '{ack}'"
    except Exception as e:
        return f"Socket demo error: {e}"
