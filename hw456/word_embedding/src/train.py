# -*- coding: utf-8 -*-

import logging
import os

from gensim.models import word2vec
from tqdm import tqdm

DATA_PATH = '../preprocess'
DATA_NAME = 'wiki_trial_seg_userstops.txt'
TRIAL_DATA_NAME = 'trial_seg_userstops.txt'

MODEL_PATH = '../model'
MODEL_NAME = 'wiki_trial_userstops_emb_128.model'
def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    #first training
    # sentences = word2vec.LineSentence(os.path.join(DATA_PATH, DATA_NAME))
    # model = word2vec.Word2Vec(sentences, window=5, size=128)
    # model.save(os.path.join(MODEL_PATH, MODE_NAME))

    #second_training
    SecondTrain(os.path.join(MODEL_PATH, MODEL_NAME), os.path.join(DATA_PATH, TRIAL_DATA_NAME))


def SecondTrain(model_loc, train_data_loc):
    model = word2vec.Word2Vec.load(model_loc)
    sentences = word2vec.LineSentence(train_data_loc)
    wv = model.wv

    model.train(sentences,total_examples=model.corpus_count, epochs=5)
    model.save('./wiki_trial_userstops_emb_128_secondtrain.model')

if __name__ == "__main__":
    main()
