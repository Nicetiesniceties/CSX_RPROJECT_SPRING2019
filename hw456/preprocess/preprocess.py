import numpy as np
import os, re
import jieba 
from hanziconv import HanziConv
import json
from zhon import hanzi
from tqdm import tqdm

abs_dir = "."
PATH = "./insult_data"

Stop_Words = open(os.path.join(abs_dir, 'stops.txt')).read().split('\n')
remove = ['─', '│', '┼', '┌', '┬', '┐', '└', '┴', '-', '┘', '├', '┤', "○", "×"]

def textClean(text):
    text = re.sub(r"[^A-Za-z]", " ", text)
    # text = [w for w in text if len(w) > 1]
    text = list(set(text))  
    text = " ".join(text)
    return(text) 

def Segmentation(tmp):
	tmp = [i for i in tmp if i not in remove]
	tmp = ''.join(tmp)
	tmp = ' '.join(re.findall('[{}]'.format(hanzi.characters+"0123456789."), tmp))

	# seg_list = jieba.cut_for_search(tmp)
	seg_list = jieba.cut(tmp, cut_all=False)
	seg_list = [x for x in seg_list if x != "," and x not in Stop_Words]
	print("Output: " + "/ ".join(seg_list))





# tmp_file = "CHDM,107,交簡,1216,20180531,1.json"
# tmp_file = "ULDM,99,訴,153,20100420,2.json"
# tmp_file = "ULDM,99,易,200,20100416,1.json"
word_list = []
# trivial = ["切勿逕送上級法院", "傳聞法則", "敘述具體上訴理由", "想像競合犯"]


DICT = dict()
file = open("namelist")
for line in tqdm(file):
	# print(line)
	with open(os.path.join(PATH, line.strip("\n"))) as fp:
	    data = json.load(fp)
	# Segmentation(data['JFULL'])

	a = data['JFULL']
	
	beg = None
	while 1:
		if beg == None:
			up = a.find("「")
		else:
			up = a.find("「", beg)
		if up == -1:
			break
		down = a.find("」", up)
		beg = up+1
		if down - up < 20:	
			target = a[up:down+1]
			# word_list.append(target)
			# print(target)
			target = ''.join(re.findall('[{}]'.format(hanzi.characters+"，、"), target))
			if(target in DICT.keys()):
				DICT[target] += 1
			else:
				DICT[target] = 1
			# print(target)
		# t.append((up, down))
		# print(t)
	# input()
	np.save("raw_with_freq.npy", DICT)
	# embed()
