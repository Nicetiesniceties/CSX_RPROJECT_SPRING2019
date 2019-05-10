import os
import numpy as np
from gensim.models import word2vec

MODEL_PATH = '../model'
DATA_PATH = '../preprocess'
MODEL_NAME = 'wiki_trial_userstops_emb_128.model'
ZH_NAME = 'new_ZH.txt'
TRIAL_NAME = 'trial_seg_userstops.txt'

#Get the 5 most similar words with each word in ZH
def MostSimZH(wv, ZH_set):
    output = open('most_sim_by_ZH.txt', 'w', encoding='utf-8')
    for ZH_word in ZH_set:
        if ZH_word in wv.vocab:
            output.write('{}: '.format(ZH_word))
            for word in wv.most_similar(ZH_word):
                output.write('{}: {}'.format(word[0], word[1]))
                output.write(', ')
            output.write('\n')
    output.close()

#Find ZH in trail
#using cosine similarity
def SimInTrail(wv, ZH_set, sim_threshold = 0.6):
    output = open('ZH_in_trail_secondtrain.txt', 'w', encoding='utf-8')
    is_find = False
    with open(os.path.join(DATA_PATH, TRIAL_NAME), 'r', encoding='utf-8') as fp:
        for content in fp.readlines():
            for word in content.split(' '):
                for ZH_word in ZH_set:
                    if word in wv.vocab:
                        sim = wv.similarity(word, ZH_word)
                        if sim >= sim_threshold:
                            if not is_find:
                                output.write('{}: '.format(word))
                                is_find = True
                            output.write('({}, {})'.format(ZH_word, sim))
            if is_find:
                output.write('\n')
                is_find = False
    output.close()

def main():

    #load model and get ZH set
    ZH_set = set()
    model = word2vec.Word2Vec.load(os.path.join(MODEL_PATH, MODEL_NAME))
    wv = model.wv
    with open(os.path.join(DATA_PATH, ZH_NAME), 'r', encoding='utf-8') as ZH_words:
        for ZH_word in ZH_words:
            ZH_word = ZH_word.strip('\n')
            if ZH_word in wv.vocab:
                ZH_set.add(ZH_word)

    #find similarity
    # SimInTrail(wv, ZH_set)
    MostSimZH(wv, ZH_set)
        

if __name__ == "__main__":
    main()
