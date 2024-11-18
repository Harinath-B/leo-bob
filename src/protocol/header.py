# src/protocol/header.py

import struct
import socket

class AstroLEOHeader:
    HEADER_FORMAT = "!BBH4sH4sHIQ"  # Header fields: version, type, IPs, ports, sequence, timestamp
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, version_major, version_minor, message_type, dest_ipv4, dest_port, source_ipv4, source_port, sequence_number, timestamp):
        self.version_major = version_major
        self.version_minor = version_minor
        self.message_type = message_type
        self.dest_ipv4 = socket.inet_aton(dest_ipv4)  # Convert IPv4 to bytes
        self.dest_port = dest_port
        self.source_ipv4 = socket.inet_aton(source_ipv4)  # Convert IPv4 to bytes
        self.source_port = source_port
        self.sequence_number = sequence_number
        self.timestamp = timestamp

    def encode(self):
        """Encodes the header into bytes for transmission."""
        return struct.pack(
            self.HEADER_FORMAT,
            self.version_major,
            self.version_minor,
            self.message_type,
            self.dest_ipv4,
            self.dest_port,
            self.source_ipv4,
            self.source_port,
            self.sequence_number,
            self.timestamp
        )

    @staticmethod
    def decode(data):
        """Decodes bytes into an AstroLEOHeader object."""
        fields = struct.unpack(AstroLEOHeader.HEADER_FORMAT, data[:AstroLEOHeader.HEADER_SIZE])
        return AstroLEOHeader(
            version_major=fields[0],
            version_minor=fields[1],
            message_type=fields[2],
            dest_ipv4=socket.inet_ntoa(fields[3]),
            dest_port=fields[4],
            source_ipv4=socket.inet_ntoa(fields[5]),
            source_port=fields[6],
            sequence_number=fields[7],
            timestamp=fields[8]
        )
