import numpy as np
raw = np.load("raw_with_freq.npy").item()
for i in list(raw.keys()):
	if len(i) > 8:
		del(raw[i])
print(raw)
print(len(list(raw.keys())))
np.save("shorten_raw_with_freq.npy", raw)
