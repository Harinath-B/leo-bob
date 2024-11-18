# src/main.py

from network.satellite_node import SatelliteNode
from config import node_config
import threading
import time

def main(node_id):
    node_info = node_config.get(node_id)
    if not node_info:
        print(f"[ERROR] Node ID {node_id} not found.")
        return
    
    satellite = SatelliteNode(
        node_id=node_id,
        ip=node_info["ip"],
        communication_port=node_info["port"]
    )
    
    satellite.start_all_services()
    
    # time.sleep(5)
    
    # satellite.send_data_message(2, "Hello from 1 to 2")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <node_id>")
        sys.exit(1)
    
    node_id = int(sys.argv[1])
    main(node_id)
