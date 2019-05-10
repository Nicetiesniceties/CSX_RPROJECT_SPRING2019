import os
import numpy as np
from tqdm import tqdm
from gensim.models import Word2Vec
from IPython import embed
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import random as rd

abs_dir = "."

def main():
    Stop_Words = open(os.path.join(abs_dir, 'stops.txt')).read().split('\n')

    out = np.load("jieba_word_after_stopword.npy").tolist()
    ZH_dict_clean = np.load("clean_with_freq.npy").item()
    ZH = list(ZH_dict_clean.keys())

    
    model = Word2Vec(out, size=128, window=5, min_count=3, workers=8)
    model.save("word2vec1.model")
    model = Word2Vec.load("word2vec1.model")

    vectors = model.wv
    # vectors.vocab
    all_words = list(vectors.vocab.keys())

    ZHN = [w for w in ZH if w in all_words]

    embedding_zh = np.array([np.array(vectors[i]) for i in ZHN])

    Not_ZH = [w for w in all_words if w not in ZHN] 
    
    embedding_n = np.array([np.array(vectors[i]) for i in Not_ZH])
    embedding_n_sample = np.array(rd.sample(list(embedding_n), 40000))

    embedding = np.concatenate((embedding_zh, embedding_n_sample), axis=0)

    ZH_len = embedding_zh.shape[0]
    # pca = PCA(32,True,True)
    # embedding = pca.fit_transform(embedding)

    embedding = TSNE(n_components = 2).fit_transform(embedding) 
    # np.save("TSNE.npy", embedding)
    # embedding = np.load("TSNE.npy")

    plt.scatter(embedding[:ZH_len,0], embedding[:ZH_len,1], c = 'b', label = 'ZH', s = 0.2)
    plt.scatter(embedding[ZH_len:,0], embedding[ZH_len:,1], c = 'r', label = 'Not ZH', s = 0.2)
    plt.legend()
    plt.savefig("./tsne.png")
    # plt.gcf().clear()

    

if __name__ == '__main__':
    main()