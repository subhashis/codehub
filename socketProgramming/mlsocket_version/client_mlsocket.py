import socket
from mlsocket import MLSocket
import glob, os
import numpy as np

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def send_numpy_array(fname, data):
	# Send data
	with MLSocket() as s:
	    s.connect(ADDR) # Connect to the port and host
	    #Sending the filename to the server
	    s.send(fname.encode(FORMAT))
	    msg = s.recv(SIZE).decode(FORMAT)
	    print(f"[SERVER]: {msg}")
	    s.send(data) 


def append_new_line(file_name, text_to_append, flen):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        if flen > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def get_filelist(file_name):
	with open(file_name) as f:
	    content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	return content


def main():
	#get into the client data directory
	os.chdir("./client_npy_data")

	#obtain the list of already transferred files, we will not copy this files 
	flist = get_filelist("transferred_files.txt")
	num_files_transferred = len(flist)	

	#go through all .npy files
	for file in glob.glob("*.npy"):
		#skip the once already transferred
		if file not in flist:
			print("transferring: ", file)
			data = np.load(file)
			#transfer the file to server
			send_numpy_array(file, data)

			#update the list of transferred files
			append_new_line("transferred_files.txt", file, num_files_transferred)
			flist = get_filelist("transferred_files.txt")
			num_files_transferred = len(flist)
	

if __name__ == "__main__":
    main()