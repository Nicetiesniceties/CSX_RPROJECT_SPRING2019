import numpy as np
import pandas as pd
DICT = np.load("clean_with_freq.npy").item()
DICT = dict(sorted(DICT.items(), key=lambda x: x[1], reverse = True))
key = list(DICT.keys())
freq = list(DICT.values())
year_dict = np.load("zh_year_table.npy").item()
# print(len(key), len(year_dict))
year = []
for i in key:
	if(i in year_dict.keys()):
		year.append(year_dict[i])
	else:
		year.append("0")
df = pd.DataFrame({"keys": key, "frequency": freq, "year": year})
print(df)
df.to_csv("HU_dictionary.csv", sep=',')
