import socket
from mlsocket import MLSocket
import numpy as np

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def main():
	print("[STARTING] Server is starting...")
	with MLSocket() as s:
	    s.bind(ADDR)
	    s.listen()
	    print("[LISTENING] Server is listening...")
	    while True:
		    conn, address = s.accept()
		    print(f"[NEW CONNECTION] {address} connected.")

		    with conn:
		    	#Receiving the filename from the client
		        filename = conn.recv(SIZE).decode(FORMAT)
		        print(f"[RECV] Receiving the filename.")
		        print(filename)		    	
	        	conn.send("Filename received.".encode(FORMAT))

		        data = conn.recv(1024) # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
		        np.save("server_npy_data/"+filename, data)
		        print("SERVER: Successfully stored np array of shape", data.shape, " to server_npy_data/" + filename)
		        
		    print("[LISTENING] Server is listening...")

if __name__ == "__main__":
    main()