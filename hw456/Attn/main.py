import argparse
import os
import torch
import jieba
import json
import numpy as np
from src.train import trainIters
from src.evaluate import runTest
from IPython import embed
from time import time
from gensim.models import Word2Vec

max_length = 1000


def Segmentation(tmp, Stop_Words):
    seg_list = jieba.cut_for_search(tmp)
    seg_list = jieba.cut(tmp, cut_all=False)
    seg_list = [x for x in seg_list]  # if x != "," and x not in Stop_Words]
    # print("Output: " + "/ ".join(seg_list))
    return seg_list


def DataFilter(data_list, Stop_Words):
    out = []
    for i in data_list:
        if i[0] == "<":
            out.extend([i[1:-1]])
        else:
            out.extend(Segmentation(i, Stop_Words))
    return out


def LoadData(args):
    file = open("namelist")
    Stop_Words = open("stops.txt").read().split('\n')
    cou, t0, Out, Length = 0, time(), [], []
    for line in (file):
        cou += 1
        with open(os.path.join(args.data_path, line.strip("\n"))) as fp:
            data = json.load(fp)
        if len(data) > 400:
            # print(len(data))
            continue
        data = DataFilter(data, Stop_Words)
        if len(data) <= max_length:
            Out.append(data)
            Length.append(len(data))
        if cou % 100 == 0:
            print(">> ", cou, len(Length))
        if len(Length) > 3000:
            break
    print("Cost time: {}".format(time()-t0))
    return Out


def parse():
    parser = argparse.ArgumentParser(description=
                                     'Attention Seq2Seq Chatbot')
    parser.add_argument('-dp', '--data_path', type=str,
                        default="../../new/modify",
                        help='Modify Data Path (After label ZH)')
    parser.add_argument('-lr', '--learning_rate', type=float,
                        default=0.0001, help='Learning rate')
    parser.add_argument('-b', '--batch_size', type=int,
                        default=50, help='Batch size')
    parser.add_argument('-la', '--n_layers', type=int, default=1,
                        help='Number of layers in encoder and decoder')
    parser.add_argument('-hi', '--hidden_size', type=int,
                        default=128, help='Hidden size in encoder and decoder')
    parser.add_argument('-p', '--print_every', type=int,
                        default=100, help='Print every p iterations')
    parser.add_argument('-s', '--save_every', type=int,
                        default=500, help='Save every s iterations')
    parser.add_argument('-d', '--dropout', type=float, default=0.2,
                        help='Dropout probability for rnn and dropout layers')
    parser.add_argument('-ep', '--epoch', type=int,
                        default=5, help='Number of epoch')

    args = parser.parse_args()
    return args


def main(args):
    if os.path.exists("VD.npy"):
        data = np.load("VD.npy")
    else:
        data = LoadData(args)

    data = data.tolist()
    for i in range(len(data)):
        while len(data[i]) < max_length:
            data[i].append("<PAD>")

    # model = Word2Vec(data, size=64, window=5, min_count=1, workers=32)
    # model.save("word2vec1.model")

    model = Word2Vec.load("word2vec1.model")

    vectors = model.wv
    all_words = list(vectors.vocab.keys())
    trainIters(data, args.learning_rate, args.batch_size, args.n_layers,
               args.hidden_size, args.print_every, args.save_every,
               args.dropout, args.epoch, max_length)

if __name__ == '__main__':
    args = parse()
    # run(args)
    main(args)
