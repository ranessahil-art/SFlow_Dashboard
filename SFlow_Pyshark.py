import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import pyshark, requests
from datetime import datetime
from Sflow_Device_SQL import insert_device

SFLOW_PORT = 6343

# Automatically detect first interface
INTERFACE = "Ethernet"

packet_count = 0

capture = pyshark.LiveCapture(
    interface=INTERFACE,
    bpf_filter=f"udp port {SFLOW_PORT}"
)

print(f"Listening for sFlow packets on UDP port {SFLOW_PORT}...")
print(f"Interface : {INTERFACE}")

for pkt in capture.sniff_continuously():


    try:

        packet_count += 1

        print("\n" + "=" * 100)
        print("sFlow Packet Received")
        print("=" * 100)

        print("Packet Number :", packet_count)
        print("Time          :", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

        print("\nLAYERS DETECTED")
        print("-" * 60)

        for layer in pkt.layers:
            print(layer.layer_name)

        print("\nFULL PYSHARK DECODE")
        print("-" * 60)

        for layer in pkt.layers:

            print("\n" + "=" * 80)
            print(f"LAYER : {layer.layer_name.upper()}")
            print("=" * 80)

            print(layer)

        if hasattr(pkt, "sflow"):


         print("\nSFLOW FIELD NAMES")
         print("-" * 60)
         print(pkt.sflow.field_names)

         from SFlow_Device import device_info

         device = device_info

         print("\n========== DEVICE INFORMATION ==========\n")

         for key, value in device.items():
          print(f"{key} : {value}")



    except Exception as e:
        print("\nError Processing Packet")
        print(e)