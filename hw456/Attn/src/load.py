import torch
import re
import os
import unicodedata
from IPython import embed


SOS_token = 0
EOS_token = 1
PAD_token = 2


class Voc:
    def __init__(self, name):
        self.name = name
        self.word2index = {"SOS": 0, "EOS": 1, "PAD": 2}
        self.word2count = {"SOS": 0, "EOS": 0, "PAD": 0}
        self.index2word = {0: "SOS", 1: "EOS", 2: "PAD"}
        self.n_words = 3  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


# Turn a Unicode string to plain ASCII, thanks to
# http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s


def readVocs(corpus, corpus_name):
    print("Reading lines...")

    # combine every two lines into pairs and normalize
    with open(corpus) as f:
        content = f.readlines()
    # import gzip
    # content = gzip.open(corpus, 'rt')

    # lines = [x.strip() for x in content]
    lines = [x.strip().split(",") for x in content]

    # it = iter(lines)
    # # pairs = [[normalizeString(x), normalizeString(next(it))] for x in it]
    # pairs = [[x, next(it)] for x in it]

    pairs = [[x[4:], y[4:]] for x, y in lines]  # remove "SOS "
    # embed()

    voc = Voc(corpus_name)
    return voc, pairs


def filterPair(p, max_length):
    # input sequences need to preserve the last word for EOS_token
    return len(p[0].split(' ')) < max_length and \
        len(p[1].split(' ')) < max_length


def filterPairs(pairs, max_length):
    return [pair for pair in pairs if filterPair(pair, max_length)]


def prepareData(corpus, corpus_name, max_length, save_dir):
    voc, pairs = readVocs(corpus, corpus_name)
    print("Read {!s} sentence pairs".format(len(pairs)))

    pairs = filterPairs(pairs, max_length)
    # print("NOT Trimmed :P")

    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
    print("Counted words:", voc.n_words)
    directory = os.path.join(save_dir, corpus_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    torch.save(voc, os.path.join(directory, '{!s}.tar'.format('voc')))
    torch.save(pairs, os.path.join(directory, '{!s}.tar'.format('pairs')))
    return voc, pairs


def loadPrepareData(corpus, max_length, save_dir):
    corpus_name = corpus.split('/')[-1].split('.')[0]
    try:
        print("Start loading training data ...")
        voc = torch.load(os.path.join(save_dir, corpus_name, 'voc.tar'))
        pairs = torch.load(os.path.join(save_dir, corpus_name, 'pairs.tar'))
    except FileNotFoundError:
        print("Saved data not found, start preparing trianing data ...")
        voc, pairs = prepareData(corpus, corpus_name, max_length, save_dir)
    return voc, pairs
