import pandas as pd
df = pd.read_excel("new_HU_dictionary.xlsx")
key_list = []
for i in range(len(df["keys"])):
	if(df["frequency"][i] > 1):
		key_list.append(df["keys"][i])
key_list = sorted(key_list, key = len, reverse = True)
for i in key_list:
	if(i == "謀"):
		break
	print(i)
