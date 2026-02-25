import socket
import threading
import datetime
from bson import BSON
from NetGarden.CORE.Packet import Packet

class Proxy:
    def __init__(self, listen_host, listen_port, server_host, server_port, on_packet, on_log, on_close=None):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.server_host = server_host
        self.server_port = server_port
        self.on_packet = on_packet
        self.on_log = on_log
        self.on_close = on_close
        self._thread = None
        self._stop_flag = threading.Event()

    def log(self, msg):
        if self.on_log:
            self.on_log(msg)

    def start(self):
        self._stop_flag.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_flag.set()

    def _now_ts(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _run(self):
        server_sock = None
        client_sock = None
        listener = None

        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.listen_host, self.listen_port))
            listener.listen(1)

            self.log(f"[NetGarden] Listening on {self.listen_host}:{self.listen_port}")

            client_sock, addr = listener.accept()
            client_sock.settimeout(None)
            self.log(f"[NetGarden] Client connected: {addr}")

            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.settimeout(10)
            server_sock.connect((self.server_host, self.server_port))
            server_sock.settimeout(None)
            self.log(f"[NetGarden] Connected to server {self.server_host}:{self.server_port}")

            t1 = threading.Thread(target=self._pipe, args=(client_sock, server_sock, "client"), daemon=True)
            t2 = threading.Thread(target=self._pipe, args=(server_sock, client_sock, "server"), daemon=True)
            t1.start()
            t2.start()

            while not self._stop_flag.is_set():
                if not t1.is_alive() or not t2.is_alive():
                    break
                threading.Event().wait(0.1)

        except Exception as e:
            self.log(f"[ERROR] Proxy run error: {e}")

        finally:
            for s in (client_sock, server_sock, listener):
                try:
                    if s:
                        s.close()
                except:
                    pass

            try:
                if self.on_close:
                    self.on_close()
            except:
                pass

    def _pipe(self, source, destination, direction):
        buffer = bytearray()

        try:
            while not self._stop_flag.is_set():
                chunk = source.recv(4096)
                if not chunk:
                    self.log(f"[NetGarden] Pipe closed by peer: {direction}")
                    break

                buffer.extend(chunk)

                while True:
                    if len(buffer) < 4:
                        break

                    length = int.from_bytes(buffer[0:4], "little", signed=False)

                    if length < 4 or length > 5_000_000:
                        self.log(f"[ERROR] Invalid length={length} ({direction}), resetting buffer")
                        buffer.clear()
                        break

                    if len(buffer) < length:
                        break

                    frame = bytes(buffer[:length])
                    del buffer[:length]

                    bson_data = frame[4:]

                    parsed = None
                    packet_id = "?"
                    try:
                        parsed = BSON(bson_data).decode()
                        if isinstance(parsed, dict) and "ID" in parsed:
                            packet_id = str(parsed.get("ID"))
                    except Exception as e:
                        self.log(f"[WARN] BSON decode failed ({direction}): {e}")

                    pkt = Packet(direction, frame, parsed, packet_id=packet_id, timestamp=self._now_ts())
                    self.on_packet(pkt)
                    destination.sendall(frame)

        except Exception as e:
            self.log(f"[ERROR] Pipe error ({direction}): {e}")