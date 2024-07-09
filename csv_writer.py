import socket
import csv

HOST = '192.168.1.141'
PORT = 80

filename = "data.csv"

fields = ['ultrasonic', 'a/g1', 'a/g2', 'a/g3', 'a/g4', 'a/g5', 'a/g6']

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to Server at {HOST} : {PORT}")

        # Open the CSV file in write mode and create a CSV writer object
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(fields)  # Write the headers

            while True:
                data = s.recv(1024).decode('utf-8').strip()

                if data:
                    print(f"Data received: {data}")

                    # Split the received data by new lines to handle multiple lines of input
                    lines = data.split('\n')
                    for line in lines:
                        if line:
                            parts = line.split(',')
                            if len(parts) == 2:
                                ultrasonic = parts[0].strip()
                                ag_values = parts[1].replace('a/g:', '').strip().split()
                                if len(ag_values) == 6:
                                    # Combine ultrasonic and a/g values into one row
                                    row = [ultrasonic] + ag_values
                                    print(f"Writing row: {row}")
                                    writer.writerow(row)

receive_data()
