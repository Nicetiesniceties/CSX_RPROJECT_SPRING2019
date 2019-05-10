import numpy as np
import pandas as pd
import os, re
import jieba 
from hanziconv import HanziConv
import json
from zhon import hanzi
from tqdm import tqdm
# from IPython import embed
from time import time

abs_dir = "."
PATH = "./insult_data"

Stop_Words = open(os.path.join(abs_dir, 'stops.txt')).read().split('\n')
remove = ['─', '│', '┼', '┌', '┬', '┐', '└', '┴', '-', '┘', '├', '┤', "×"] # , "○"


def Flatten_list(l):
    def Flatten_list_recur(l, output):
        if type(l) is not list and l != "":
            output.append(l)
            return
        for item in l:
            Flatten_list_recur(item, output)
        
    output = []
    Flatten_list_recur(l, output)
    return output

def process_list(l): # split by ，。、
    l = [i.split("，") for i in l]
    l = Flatten_list(l)
    l = [i.split("、") for i in l]
    l = Flatten_list(l)
    l = [i.split("。") for i in l]
    l = Flatten_list(l)
    return l

def process_list_ZH(l, Sorted_keys):
    return_list = []
    flag = False
    for cou, i in enumerate(l):
        out = [i]
        for z in Sorted_keys:
            if len(i.split(z)) != 1:
                flag=True
                out = i.split(z)
                out.insert(1, "<"+z+">")
                # print(out)
                # print(z)
                break
        return_list.extend(out)
        # print(return_list)
    if flag == False:
        # print("NO ZH")
        return None
    return_list = [i for i in return_list if i != ""]
    return return_list

def Split_ZH_Ver2(tmp, Sorted_keys): # per sentence
    tmp2 = ''.join([i for i in tmp if i not in remove])
    tmp2 = ''.join(re.findall('[{}]'.format(hanzi.characters+"0123456789，。、\n"), tmp2))
    tmp2 = tmp2.split("\n")
    # print(tmp2[:6])
    if "主文" not in tmp2 and "一、主文" not in tmp2:
        return None
    elif "主文" in tmp2:
        split_id = tmp2.index("主文")
        t1 = tmp2[:split_id+1]
        t2 = tmp2[split_id+1:]

    elif "一、主文" in tmp2:
        split_id = tmp2.index("一、主文")
        t1 = tmp2[:split_id+1]
        t2 = tmp2[split_id+1:]

    t1 = process_list(t1) # before "主文" no "，。、", only have \n
    t2 = ["".join(t2)]
    t2 = process_list(t2)
    t2 = process_list_ZH(t2, Sorted_keys)
    
    if t2 == None:
        return None
    # print(t1+t2)
    return t1+t2


def main():
    Keys = []
    f = open("new_ZH.txt")
    for line in f:
        Keys.append(line.strip())
    Keys = list(set(Keys))
    Sorted_keys = sorted(Keys, key=len, reverse=True)

    file = open("namelist")
    Dict = {}
    counter = 0
    t00 = time();t0 = time()
    for line in tqdm(file):
        Verdict_list = []
        with open(os.path.join(PATH, line.strip("\n"))) as fp:
            data = json.load(fp)
        a = data['JFULL']

        word_list = Split_ZH_Ver2(a, Sorted_keys)
        if (word_list) != None:
            Verdict_list.append(word_list)
            # print(word_list)

        counter+=1
        if counter%1000 == 0:
            print(counter, time() - t0, len(Verdict_list))
            t0 = time()
        with open('./modify/' + line, 'w+') as outfile:
            json.dump(Verdict_list, outfile, ensure_ascii=False)
        # file = open("./modify/" + line + ".txt", "w+")
        # for i in Verdict_list:
        #     file.write(i)
	 

    print("All consuming time: ", time() - t00)
    # put into for loop
    # np.save("jieba_word_after_stopword.npy", Verdict_list)

if __name__ == '__main__':
    main()
