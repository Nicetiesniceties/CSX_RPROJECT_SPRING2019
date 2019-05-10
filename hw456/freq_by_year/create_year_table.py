import numpy as np
from tqdm import tqdm
PATH = "./zh2year/"
# th_year_distribution_dict.npy
ZH_year_table = dict()
SUM = 0
for i in range(85, 108):
	temp = np.load(PATH + str(i) + "th_year_distribution_dict.npy").item()
	keys = list(temp.keys())
	SUM += len(keys)
	print(i)
	for j in keys:
		print(j)
		if(j in ZH_year_table.keys()):
			ZH_year_table[j] = str(ZH_year_table[j]) + "/" + str(i)
		else:
			ZH_year_table[j] = str(i)
print(ZH_year_table)
np.save("zh_year_table.npy", ZH_year_table)
