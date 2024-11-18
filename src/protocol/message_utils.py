# src/protocol/message_utils.py

import socket
from protocol.header import AstroLEOHeader
import socket

def send_message(header, data, dest_ip, dest_port):
    """Encodes and sends a message over UDP."""
    message = header.encode() + data.encode('utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, (dest_ip, dest_port))
    print(f"[INFO] Sent message to {dest_ip}:{dest_port}")

def receive_message(sock):
    """Receives and decodes a message."""
    data, addr = sock.recvfrom(1024)
    header = AstroLEOHeader.decode(data[:AstroLEOHeader.HEADER_SIZE])
    payload = data[AstroLEOHeader.HEADER_SIZE:].decode('utf-8')
    return header, payload, addr
