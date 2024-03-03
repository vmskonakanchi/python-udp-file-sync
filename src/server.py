import os
import sys
import socket

MAX_BUFFER_SIZE = 1024 * 4  # 4KB

if len(sys.argv) != 3:
    print(f'Usage : python {sys.argv[0]} <folder_name> <port>')
    sys.exit(1)

host = '127.0.0.1'
folder_name = sys.argv[1]
port = int(sys.argv[2])

# Set up a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))
# Set a timeout for the server socket
server.settimeout(1)  # 1 second

# Create a folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f'File Sync Server started at {host}:{port}')

# Listen for incoming connections
try:
    while True:
        try:
            data, addr = server.recvfrom(MAX_BUFFER_SIZE)
            data = data.decode()

            file_name, content = data.split('-')
            file_path = os.path.join(folder_name, os.path.basename(file_name))

            if not content:
                print('No content received!')
                continue

            if not os.path.exists(file_path):
                open(file_path, 'w').close()
            
            with open(file_path, 'wb') as file:
                file.write(content.encode())

            server.sendto('OK'.encode(), addr)
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print('File Sync Server closed! Bye Bye!')
            break
except Exception as e:
    print('An error occurred:', str(e))
finally:
    server.close()
