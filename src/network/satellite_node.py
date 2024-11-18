# src/network/satellite_node.py

import threading
from protocol.message_types import create_discovery_message, create_data_message
from protocol.message_utils import send_message, receive_message
from config import node_config
import time
import socket

class SatelliteNode:
    def __init__(self, node_id, ip, communication_port):
        self.node_id = node_id
        self.ip = ip
        self.communication_port = communication_port  # Unique port for data messages
        self.discovery_port = 33000  # Shared port for discovery messages
        self.running = True

    def start_discovery_broadcast(self):
        """Sends a periodic discovery message to the shared discovery port."""
        sequence_number = 1
        while self.running:
            header = create_discovery_message(self.ip, self.communication_port, sequence_number)
            # Broadcast discovery message to all on discovery port
            send_message(header, "", "0.0.0.0", self.discovery_port)
            print(f"[INFO] Satellite {self.node_id} sent discovery message to port {self.discovery_port}")
            sequence_number += 1
            time.sleep(5)

    def start_discovery_listener(self):
        """Listens for incoming discovery messages on the shared discovery port."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", self.discovery_port))
            print(f"[LISTENING] Satellite {self.node_id} listening for discovery messages on port {self.discovery_port}")
            while self.running:
                header, payload, addr = receive_message(sock)
                print('[DISCOVERY CONT]', socket.inet_ntoa(header.source_ipv4), header.source_port, payload, addr)
                if header.message_type == 1:  # Discovery message
                    self.process_discovery_message(header, addr)

    def process_discovery_message(self, header, addr):
        """Processes received discovery messages."""
        print(f"[DISCOVERY] Satellite {self.node_id} discovered Satellite at {addr[0]}:{addr[1]}")
        # Here you can add the discovered satellite to a neighbors list if needed

    def start_data_listener(self):
        """Listens for incoming data messages on the satellite's unique communication port."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.ip, self.communication_port))
            print(f"[LISTENING] Satellite {self.node_id} on {self.ip}:{self.communication_port} for data messages")
            while self.running:
                header, payload, addr = receive_message(sock)
                self.process_message(header, payload)

    def send_data_message(self, dest_id, message):
        """Sends a data message to another satellite."""
        dest_info = node_config.get(dest_id)
        if not dest_info:
            print(f"[ERROR] Unknown destination ID {dest_id}")
            return
        header = create_data_message(self.ip, self.communication_port, dest_info['ip'], dest_info['port'], 1)
        send_message(header, message, dest_info['ip'], dest_info['port'])

    def process_message(self, header, payload):
        """Processes received messages based on type."""
        if header.message_type == 1:  # Discovery (handled separately in process_discovery_message)
            pass
        elif header.message_type == 2:  # Data
            print(f"[DATA] Satellite {self.node_id} received data: {payload}")
        elif header.message_type == 3:  # Ack
            print(f"[ACK] Satellite {self.node_id} received acknowledgment.")
        elif header.message_type == 4:  # Route Advertisement
            print(f"[ROUTE] Satellite {self.node_id} received route advertisement.")

    def start_all_services(self):
        """Starts the discovery broadcast, discovery listener, and data listener."""
        threading.Thread(target=self.start_discovery_broadcast).start()
        threading.Thread(target=self.start_discovery_listener).start()
        threading.Thread(target=self.start_data_listener).start()
