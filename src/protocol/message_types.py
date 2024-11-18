# src/protocol/message_types.py

import time
from protocol.header import AstroLEOHeader

# Message type constants
MESSAGE_TYPE_DISCOVERY = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_ACK = 3
MESSAGE_TYPE_ROUTE_ADVERTISEMENT = 4

# Helper functions to create each type of message with AstroLEOHeader

def create_discovery_message(source_ip, source_port, sequence_number):
    """Creates a discovery message header."""
    return AstroLEOHeader(
        version_major=1,
        version_minor=0,
        message_type=MESSAGE_TYPE_DISCOVERY,
        dest_ipv4="0.0.0.0",  # Broadcast IP for discovery
        dest_port=33000,               # Shared discovery port
        source_ipv4=source_ip,
        source_port=source_port,
        sequence_number=sequence_number,
        timestamp=int(time.time() * 1000)  # Millisecond precision
    )

def create_data_message(source_ip, source_port, dest_ip, dest_port, sequence_number):
    """Creates a data message header."""
    return AstroLEOHeader(
        version_major=1,
        version_minor=0,
        message_type=MESSAGE_TYPE_DATA,
        dest_ipv4=dest_ip,
        dest_port=dest_port,
        source_ipv4=source_ip,
        source_port=source_port,
        sequence_number=sequence_number,
        timestamp=int(time.time() * 1000)
    )

def create_ack_message(source_ip, source_port, dest_ip, dest_port, sequence_number):
    """Creates an acknowledgment message header."""
    return AstroLEOHeader(
        version_major=1,
        version_minor=0,
        message_type=MESSAGE_TYPE_ACK,
        dest_ipv4=dest_ip,
        dest_port=dest_port,
        source_ipv4=source_ip,
        source_port=source_port,
        sequence_number=sequence_number,
        timestamp=int(time.time() * 1000)
    )

def create_route_advertisement(source_ip, source_port, dest_ip, dest_port, sequence_number):
    """Creates a route advertisement message header."""
    return AstroLEOHeader(
        version_major=1,
        version_minor=0,
        message_type=MESSAGE_TYPE_ROUTE_ADVERTISEMENT,
        dest_ipv4=dest_ip,
        dest_port=dest_port,
        source_ipv4=source_ip,
        source_port=source_port,
        sequence_number=sequence_number,
        timestamp=int(time.time() * 1000)
    )
