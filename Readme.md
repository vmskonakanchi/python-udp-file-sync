### This is the simple multiple file sync application using UDP

---

> I made a protocol called VTP (Vamsi Transfer Protocol) which is used to transfer the files between the client and the server and syncing files b/w two or more clients.

---

The protocol looks like this

> filename size offset_start offset_end

---

### Example

* `test.txt 65534 6 65540` - This means that the file is test.txt, the size of the file is 65534 bytes, the offset start is 6 bytes and the offset end is 65540 bytes.

---

### Commands To Run The Application

[](https://github.com/vmskonakanchi/udp-file-sync#commands-to-run-the-application)

* To run the server

```shell
 python ./src/server.py 8080 ./storage
```

* To run the client

```shell
python ./src/client.py 8000 ./client_storage server_ip:8080
```

> Replace the server_ip with the ip address of the server

---

## `Feel free to contribute to this project and make it better`
