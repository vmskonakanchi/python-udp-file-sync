import sys,socket,os,threading

MAX_BUFFER_SIZE = 1024 * 4 # 4KB
MAX_PEICE_SIZE = 1024 * 4 # 4KB
FOLDER_CHECK_SECONDS = 5.0

if len(sys.argv) != 4:
    print(f'Usage : python {sys.argv[0]} <folder_name> <host> <port>')
    sys.exit(1)

folder_name = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# starting a udp socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# connect to the server
client.connect((host, port))
print(f'Connected to the server at {host}:{port}')

changed_files = {}
file_offsets = {}

# run a background thread to monitor the folder for changes
def monitor_folder(folder_name):
    for root, _, files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(root, file)
            changed_files[file_path] = False
            # we need to get the old file size from the file_offsets
            if file_path not in file_offsets:
                file_offsets[file_path] = 0
            else:
                file_offsets[file_path] = os.path.getsize(file_path)

# start the monitor thread in the background and check for changes every n seconds
threading.Timer(FOLDER_CHECK_SECONDS, monitor_folder, args=(folder_name,)).start()

print(f'File Sync Client started at {host}:{port}')

while True:
    for file_path , is_changed in changed_files.items():
        if is_changed:
            # the file has been changed so get the offset from offsets
            offset = file_offsets[file_path]

            with open(file_path , 'rb') as f:
                f.seek(offset)
                data = f.read(MAX_PEICE_SIZE)
                client.send(f'{file_path} {offset} {data}'.encode())
                print(f'Sent {len(data)} bytes of data to the server')
                file_offsets[file_path] = offset + len(data)
                changed_files[file_path] = False
