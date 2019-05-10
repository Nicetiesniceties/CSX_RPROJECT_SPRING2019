# coding=utf-8
import numpy as np
import os, re
import jieba 
from hanziconv import HanziConv
import json
from zhon import hanzi


abs_dir = "."
PATH = "./modify_insult_data"


def textClean(text):
    text = re.sub(r"[^A-Za-z]", " ", text)
    # text = [w for w in text if len(w) > 1]
    text = list(set(text))  
    text = " ".join(text)
    return(text) 




Stop_Words = open(os.path.join(abs_dir, 'stops.txt')).read().split('\n')
remove = ['─', '│', '┼', '┌', '┬', '┐', '└', '┴', '-', '┘', '├', '┤', "○", "×"]



# tmp_file = "CHDM,107,交簡,1216,20180531,1.txt"
tmp_file = "ULDM,99,訴,153,20100420,2.txt"
# tmp_file = "ULDM,99,易,200,20100416,1.txt"
tmp = []
with open(os.path.join(PATH, tmp_file)) as file:
    for line in file:
        senten = HanziConv.toTraditional(line.strip('\n'))
        In = [i for i in senten]
        tmp.extend(In)


tmp = [x for x in tmp if x not in remove]
tmp = ''.join(tmp)
all_s = []
tmp = ''.join(re.findall('[{}]'.format(hanzi.characters+"0123456789."), tmp))
# print(tmp)

# seg_list = jieba.cut(tmp, cut_all=True)
seg_list = jieba.cut_for_search(tmp)

seg_list = [x for x in seg_list if x != "," and x not in Stop_Words]

print("Output: " + "/ ".join(seg_list))

# print(json.dumps("After: " + "/ ".join(seg_list), ensure_ascii=False, indent=None))






