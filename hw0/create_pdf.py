import numpy as np
import os
import re
import json
from tqdm import tqdm

PATH = "/4TB/schen/insult_data"

word_list = []
distribution = dict()
hu_list = np.load("clean_with_freq.npy").item()
hu_list = sorted(hu_list, key=len, reverse=True)
file = open("./namelist")
region_list = []
for line in tqdm(file):
    # print(line)
    with open(os.path.join(PATH, line.strip("\n"))) as fp:
        data = json.load(fp)
    string = data['JFULL']
    jid = data['JID']
    if(jid.find(']') != -1):
        region = (jid.split(']')[1]).split(',')[0]
    else:
        region = jid.split(',')[0]
    #print(region)
    if(not region in distribution.keys()):
        region_list.append(region)
        distribution[region] = dict()
    zh_list = hu_list
    for i in zh_list:
        if(i in string):
            if(i in distribution[region].keys()):
                distribution[region][i] += 1
            else:
                distribution[region][i] = 1
        string = "".join(string.split(i))
    for i in region_list:
        np.save("zh2region/" + i + "_distribution_dict.npy", distribution[i])
