# -*- coding: utf-8 -*-

import jieba
import logging
# from tqdm import tqdm

DATA_PATH = '../preprocess'

#temp file
def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # jieba custom setting.
    jieba.set_dictionary('jieba/extra_dict/dict.txt.big')

    with open('new_ZH.txt', 'r', encoding='utf-8') as ZH_words:
        for ZH_word in ZH_words:
            jieba.add_word(ZH_word.strip('\n'), 3)

    # load stopwords set
    #Uncertain:stops.txt?
    stopword_set = set()
    with open('stops.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    output = open('wiki_seg_userstops.txt', 'w', encoding='utf-8')
    with open('wiki_zh_tw.txt', 'r', encoding='utf-8') as content :
        for texts_num, line in enumerate(content):
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopword_set:
                    output.write(word + ' ')
            output.write('\n')

            if (texts_num + 1) % 10000 == 0:
                logging.info("完成前 %d 行" % (texts_num + 1))
    output.close()

if __name__ == '__main__':
    main()
