import numpy as np
# defineing ZH by user command
def determine_zh(i, command, clean_data, raw_data, key_list):
	if((command in ["n", "d", "no"]) and not (command in ["yes", "y"])):
		if(key_list[i] in clean_data.keys()):
			del clean_data[key_list[i]]
	elif(command == "r"):
		print("--------revert previous one--------\n")
		print("iteration:", i - 1, "key:", key_list[i - 1], "frequency:", raw_data[key_list[i - 1]])
		command = input()
		determine_zh(i - 1, command, clean_data, raw_data, key_list)
	else:
		clean_data[key_list[i]] = raw_data[key_list[i]]

raw_data = np.load("shorten_raw_with_freq.npy").item()
raw_data = dict(sorted(raw_data.items(), key = lambda x: x[1], reverse = True))
key_list = list(raw_data.keys())
clean_data = np.load("clean_with_freq.npy").item()
initial = False
for i in range(len(key_list)):
	if(key_list[i] == list(clean_data.keys())[-1]):
		initial = True
	if(not initial):
		continue
	print("iteration:", i, "key:", key_list[i], "frequency:", raw_data[key_list[i]])
	command = input()
	determine_zh(i, command, clean_data, raw_data, key_list)
	if(i % 10 == 0):
		np.save("clean_with_freq.npy", clean_data)
		print("--------saving list--------\n")
	# print(clean_data)
