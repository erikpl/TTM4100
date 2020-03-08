import time
from socket import *
import sys
# Get the server hostname and port as command line arguments                    
# Declaring default values for hostname and port number
host = '127.0.0.1'
port = 12000
timeout = 1 # in seconds

# Overriding default values if provided as commnand line arguments
if len(sys.argv) is 3:
    host = sys.argv[1]
    port = sys.argv[2]

# Creates socket with IPv4 and UDP		
client_socket = socket(AF_INET, SOCK_DGRAM)
# Set socket timeout as 1 second
client_socket.settimeout(timeout)
# Sequence number of the ping message
ptime = 0  
# Number of packets lost
lost_packets = 0
# Saving RTTs for calculating min, max and avg
rtt_list = []
# Ping for 10 times
while ptime < 10: 
    ptime += 1
    # Format the message to be sent as in the Lab description	
    data = f'PING {ptime} '
    
    try:
	# Record the "sent time"
        sent_time = time.time()
        # Append sent_time to data per ping message spec
        data += str(sent_time)
    	# Send the UDP packet with the ping message
        client_socket.sendto(data.encode(), (host, port))
	# Receive the server response
        message, address = client_socket.recvfrom(2048) 
	# Record the "received time"
        recv_time = time.time()
	# Display the server response as an output
        print(message.decode()) 
	# Round trip time is the difference between sent and received time
        rtt = recv_time - sent_time
        # Store the RTT for calculations at the end 
        rtt_list.append(rtt)
    except:
        # Server does not respond
	# Assume the packet is lost
        print("Request timed out.")
        # Recording the number of lost packets
        lost_packets += 1
        continue

# Close the client socket
client_socket.close()

print(f'Minimum RTT: {min(rtt_list)} seconds')
print(f'Maximum RTT: {max(rtt_list)} seconds')
print(f'Average RTT: {sum(rtt_list)/len(rtt_list)} seconds')
print(f'Packet loss: {(lost_packets/10)*100}%')

