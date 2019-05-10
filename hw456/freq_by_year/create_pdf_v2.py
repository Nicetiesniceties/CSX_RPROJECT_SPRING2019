import numpy as np
import os
import re
import json
from tqdm import tqdm
import pandas as pd

PATH = "./../../../insult_data"

word_list = []
distribution = dict()
# hu_list = np.load("clean_with_freq.npy").item()
# hu_list = sorted(hu_list, key = len, reverse = True)
file = open("namelist")
df = pd.read_excel("new_HU_dictionary.xlsx")
hu_list = df['keys']
year_list = []
for line in tqdm(file):
	# print(line)
	with open(os.path.join(PATH, line.strip("\n"))) as fp:
		 data = json.load(fp)
	string = data['JFULL']
	year = data['JYEAR']
	if(not year in distribution.keys()):
		year_list.append(year)
		distribution[year] = dict()
	zh_list = hu_list
	for i in zh_list:
		if(i in string):
			if(i in distribution[year].keys()):
				distribution[year][i] += 1
			else:
				distribution[year][i] = 1
		string = "".join(string.split(i))
	for i in year_list:
		np.save("zh2year/" + i + "th_year_distribution_dict.npy", distribution[i])
# 	print(distribution)

