import numpy as np
unsorted = np.load("clean_with_freq.npy").item()
Sorted = sorted(unsorted, key=len, reverse=True)
np.save("sorted_clean.npy", Sorted)
print(Sorted)
