import socket
import matplotlib.pyplot as plt
import keyboard

HOST = '192.168.1.141'
PORT = 80

data_points = []
max_points = 50  # Set the limit for the number of data points to be plotted
plt.ion()

plt.figure(figsize=(10, 6))
plt.title("Ultrasonic Sensor Data")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
line, = plt.plot([], marker='o', linestyle='-')

paused = False

def toggle_pause():
    global paused
    paused = not paused

keyboard.add_hotkey('space', toggle_pause)

def receive_data():
    buffer = ""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print(f"Connected to server at {HOST} : {PORT}")

                while True:

                    if paused:
                        plt.pause(0.1)
                        continue
                    
                    data = s.recv(1024).decode('utf-8')
                    if not data:
                        print("No data received, breaking the loop...")
                        break

                    buffer += data
                    lines = buffer.split('\n')

                    # Keep the last incomplete line in the buffer
                    buffer = lines.pop()

                    for line_data in lines:
                        line_data = line_data.strip()
                        if line_data:
                            try:
                                value = float(line_data)
                                data_points.append(value)

                                # Keep only the last 'max_points' data points
                                if len(data_points) > max_points:
                                    data_points.pop(0)

                                line.set_xdata(range(len(data_points)))
                                line.set_ydata(data_points)
                                plt.xlim(0, max_points - 1)  # Update x-axis limit
                                plt.ylim(min(data_points) - 1, max(data_points) + 1)  # Update y-axis limit
                                plt.draw()
                                plt.pause(0.1)

                            except ValueError:
                                print(f"Invalid Data: {line_data}")

        except ConnectionError as e:
            print(f"Connection error: {e}. Reconnecting...")
            continue

receive_data()
