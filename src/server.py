import os,sys,socket,threading

MAX_CLIENTS = 5
MAX_BUFFER_SIZE = 1024 * 4 # 4KB

if len(sys.argv) != 3:
    print(f'Usage : python {sys.argv[0]} <folder_name> <port>')
    sys.exit(1)

host = '127.0.0.1'
folder_name = sys.argv[1]
port = int(sys.argv[2])

# set up a udp server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

# creating a folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f'File Sync Server started at {host}:{port}')

# listen for incoming connections

while True:
    try:
        data, addr =  server.recvfrom(MAX_BUFFER_SIZE)
        print(f'Connection from {addr} has been established!')
        data = data.decode()
        file_name, offset , content = data.split(' ')
        offset = int(offset)
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'ab') as f:
            f.seek(offset)
            f.write(content)
            print(f'Wrote {len(content)} bytes of data to {file_path}')
        server.sendto('Data received successfully'.encode(), addr)
    except KeyboardInterrupt as k:
        print('File Sync Server closed! , Bye Bye!')
        server.close()
        sys.exit(0)