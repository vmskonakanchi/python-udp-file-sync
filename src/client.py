import os
import sys
import socket
import threading
import time

MAX_PIECE_SIZE = 1024 * 4  # 4KB
FOLDER_CHECK_SECONDS = 2.0  # 2 seconds

if len(sys.argv) != 4:
    print(f'Usage : python {sys.argv[0]} <folder_name> <host> <port>')
    sys.exit(1)

folder_name = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Starting a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to the server
client.connect((host, port))
print(f'Connected to the server at {host}:{port}')

# Initialize dictionaries to store file changes and offsets
changed_files = {}
file_sizes = {}

lock = threading.Lock()

# Function to monitor the folder for changes
def monitor_folder(folder_name):
    while True:
        if lock.locked():
            continue
        lock.acquire()
        for root, _, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_path not in file_sizes:
                        file_sizes[file_path] = file_size
                        changed_files[file_path] = False
                    else:
                        if file_sizes[file_path] != file_size:
                            file_sizes[file_path] = file_size
                            changed_files[file_path] = True
                except FileNotFoundError:
                    continue

        lock.release()

        # Sleep for specified interval before checking again
        time.sleep(FOLDER_CHECK_SECONDS)

# Start the monitor thread in the background and check for changes every n seconds
threading.Thread(target=monitor_folder, args=(folder_name,), daemon=True).start()

print(f'File Sync Client started at {host}:{port}')

while True:
    if lock.locked():
        continue
    for file_path, is_changed in changed_files.items():
        if is_changed:
            print(f'File {file_path} has been changed')
            changed_files[file_path] = False
            # The file has been changed so get the offset from offsets
            with open(file_path, 'rb') as file:
                # file.seek(file_offsets[file_path])
                content = file.read(MAX_PIECE_SIZE)

            content = content.decode()
            
            if not content:
                continue
            client.send(f'{file_path}-{content}'.encode())
            print(f'Sending {len(content)} bytes of data')
            # Wait for the server to acknowledge the data
            data, _ = client.recvfrom(MAX_PIECE_SIZE)
            if data.decode() == 'OK':
                changed_files[file_path] = False
                print(f'File {file_path} has been successfully synced!')
