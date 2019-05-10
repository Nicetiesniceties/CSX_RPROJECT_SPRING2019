import numpy as np
import pandas as pd
import re
# raw = np.load("raw_dict7.npy").item()
# clean = np.load("clean_with_freq.npy").item()
df = pd.read_excel("HU_dictionary.xlsx")
new_words, new_freq, new_year = [], [], []
for i in range(len(df["keys"])):
	words = []
	key = df["keys"][i]
	if("、" in key):
		words = key.split("、")
	elif("，" in key):
		words = key.split("，")
	else:
		continue
	for j in words:
		new_words.append(j)
		new_freq.append(df["frequency"][i])
		new_year.append(df["year"][i])
	df["year"][i] = 0
# print(new_words, new_freq, new_year)

for i in range(len(new_words)):
	temp = df.index[df['keys'] == new_words[i]].values
	if(len(temp) == 0):
		df = df.append({"keys": new_words[i], "frequency": new_freq[i], "year": new_year[i]}, ignore_index=True)
	else:
		df["frequency"][temp[0]] += new_freq[i]

# modDfObj = dfObj.append({'Name' : 'Sahil' , 'Age' : 22} , ignore_index=True)
# df.index[df['BoolCol'] == True]
# df.sort_values(by=['col1'])

df = df[df["year"] != 0]

df = pd.DataFrame({"keys": df["keys"], "frequency": df["frequency"], "year": df["year"]})
df = df.reset_index(drop = True)

# saveing xlsx
writer = pd.ExcelWriter('new_HU_dictionary.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

df = pd.read_excel("new_HU_dictionary.xlsx")
print(df)
'''
for i in range(len(df["keys"])):
	if (df["frequencies"][i] == 0):
	)
'''
