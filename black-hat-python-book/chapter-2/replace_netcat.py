import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
	print("BHP Net Tool")
	print("")
	print("USage: bhpnet.py -t target_host -p port")
	print("-l --listen")
	print("-e --execute=file_to_run")
	print("-u --upload=destination")
	print("")
	print("")
	print("Examples: ")
	print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
	print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c -u=c:\\target.exe")
	print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c -e=/"cat /etc/passwd\"")
	print("echo 'ABCDEF' | ./bhpnet.py -t 192.168.0.1 -p 134")
	sys.exit(0)

def main():
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]):
		usage()

	# read the commandline options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "port", "command", "upload"])
	except getopt.GetoptError as err:
		print(str(err))
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--commandshell"):
			command = True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert(False, "Unhandled Option")

	# are we going to listen or just send data from stdin?
	if not listen and len(target) and port > 0:
		# read in the buffer from the commandline
		# this will block, so send CTRL-D if not sending input
		# to stdin
		buffer = sys.stdin.read()

		# send data off
		client_sender(buffer)

		# we are going to listen and potentially
		# upload things, execute commands, and drop a shell back
		# depending on out command line options above 
		if listen:
			server_loop()

	main()