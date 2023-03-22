import pyshark

# Define the path to the network traffic report file
file_path = "./data/network.pcapng"

# Create a FileCapture object to read the network traffic report
cap = pyshark.FileCapture(file_path)

# Define a flag to indicate whether any anomalies have been found
anomaly_found = False

# Loop through each packet in the network traffic report
for packet in cap:
    # Check for suspicious activity in the packet
    if packet.tcp.flags_push == '1':
        print("Suspicious activity detected in packet {}: PUSH flag set".format(packet.number))
        anomaly_found = True
    elif packet.tcp.flags_fin == '1' and packet.tcp.flags_ack == '0':
        print("Suspicious activity detected in packet {}: FIN flag set without ACK".format(packet.number))
        anomaly_found = True

# Close the network traffic report file
cap.close()

# Check if any anomalies were found and print a message if necessary
if anomaly_found:
    print("Anomalies detected in the network traffic report")
else:
    print("No anomalies detected in the network traffic report")



#read the file line by line


