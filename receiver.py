import socket
import matplotlib.pyplot as plt

HOST = '192.168.1.141'
PORT = 80

data_points = []

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST} : {PORT}")

        while True:
            data = s.recv(1024).decode('utf-8').strip()
            if not data:
                break

            try:
                value = float(data)
                data_points.append(value)

                plt.figure(figsize=(10, 6))
                plt.plot(data_points, marker='o', linestyle='-')
                plt.title("Ultrasonic Sensor Data")
                plt.xlabel("Time")
                plt.ylabel("Value")
                plt.grid(True)
                plt.pause(0.1)
                plt.clf()
            
            except ValueError:
                print(f"Invalid Data: {data}")

receive_data()