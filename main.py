from scapy.all import *
import sys
import threading

DSCP_TABLE = """
# Service class            | DSCP Name          | TOS Decimal   |
# --------------------------------------------------------------|
# Network control          | CS6                | 192           |
# Telephony 	           | EF                 | 184           |
# Signaling 	           | CS5                | 160           |
# Multimedia conferencing  | AF41, AF42, AF43   | 136,144,152   |
# Real-time interactive    | CS4                | 128           |
# Multimedia streaming 	   | AF31, AF32, AF33   | 104,112,120   |
# Broadcast video          | CS3                | 96            |
# Low-latency data         | AF21, AF22, AF23   | 72,80,88      | 
# OAM 	                   | CS2                | 64            |
# High-throughput data 	   | AF11, AF12, AF13   | 40,48,56      |
# Standard                 | DF                 | 0             |
# Low-priority data 	   | CS1                | 32            |
"""

PROGRAM_USAGE = """
    The general form of the command used to start the program is as follows:

        python3 main.py '<tos_decimal_1>:<Mbps_value_1>' ... '<tos_decimal_X>:<Mbps_value_X>' '<destination_ip_address>'

    Where <tos_decimal> are values from the table above

    e.g: python3 main.py "192:10" "0:10" "32:10" "192.168.0.112"
"""

def generate_packet(tos, packet_size=1200, destination="127.0.0.1"):
    packet = Ether()/IP(dst=destination, tos=tos)/UDP()
    return packet/Raw('a'*(packet_size-len(packet))) #packet padded to length with 'a'

def start_sending_packets(tos, packet_size=1200, destination="127.0.0.1", mbps=10, number_of_packets=10000):
    packet = generate_packet(tos, packet_size, destination)
    print(f"Started sending packets ToS={str(tos)}")
    sendpfast(packet, mbps=mbps, loop=number_of_packets)
    print(f"Sending packets for ToS={str(tos)} has ended")

def create_threads(generators, destination):
    thread_array = []
    for generator in generators:
        gen_parameters = generator.split(":")
        thread = threading.Thread(target=start_sending_packets, kwargs={"tos":int(gen_parameters[0]), "destination":destination, "mbps":int(gen_parameters[1])})
        thread_array.append(thread)
    return thread_array

def main(args):
    if len(args)<2:
        print(DSCP_TABLE)
        print(PROGRAM_USAGE)
        return
    for thread in create_threads(args[1:-1], args[-1]):
        thread.start()
        

main(sys.argv)
