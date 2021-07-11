import numpy as np


noa = 10
fname_str = 'client_npy_data/rand_array_'

for i in range(noa):
	temp_array = np.random.random(size = (100,20))
	np.save(fname_str+str(i)+".npy", temp_array)