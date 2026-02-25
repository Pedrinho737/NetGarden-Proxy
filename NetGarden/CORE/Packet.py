class Packet:
    def __init__(self, direction, raw_frame, parsed, packet_id="?", timestamp=""):
        self.direction = direction
        self.raw = raw_frame
        self.parsed = parsed
        self.id = packet_id
        self.timestamp = timestamp
