import torch
import torch.nn as nn
from torch import optim
import torch.backends.cudnn as cudnn

import itertools
import random
import math
import os
import numpy as np
from tqdm import tqdm
from IPython import embed
from src.load import loadPrepareData
from src.load import SOS_token, EOS_token, PAD_token
from src.model import *
from src.evaluate import evaluateRandomly
from gensim.models import Word2Vec

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

cudnn.benchmark = True

#############################################
# Prepare Training Data
#############################################


def batch2TrainData(batch, max_length):
    model = Word2Vec.load("word2vec1.model")
    out = []
    vectors = model.wv
    for pair in batch:
        out.append([vectors[i] for i in pair])
        # embed()
    out = torch.LongTensor(out)
    return out


#############################################
# Training
#############################################

def trainIters(data, learning_rate, batch_size, n_layers, hidden_size,
               print_every, save_every, dropout, epoch, max_length):

    print("device: {}".format(device))

    print("Numbers of data: {}".format(len(data)))

    # training data
    all_steps = len(data)//batch_size
    try:
        training_batches = torch.load('train_data.tar')
    except FileNotFoundError:
        print('Training pairs not found, generating ...')
        training_batches = []

        for i in range(all_steps):
            b = data[batch_size*i:batch_size*(i+1)]
            training_batches.append(batch2TrainData(b, max_length))

        torch.save(training_batches, 'train_data.tar')

    random_answer = torch.randint(0, 2,
                                  (len(training_batches), batch_size)).long()

    # model
    checkpoint = None
    print('Building encoder and decoder ...')
    # RNNmodel = RNN(hidden_size, 2, max_length, n_layers, dropout)
    RNNmodel = AttnRNN(hidden_size, 2, max_length, n_layers, dropout)

    # if loadFilename:
    #     checkpoint = torch.load(loadFilename)
    #     encoder.load_state_dict(checkpoint['en'])

    # use cuda
    RNNmodel = RNNmodel.to(device)

    # optimizer
    print('Building optimizers ...')
    optimizer = optim.Adam(RNNmodel.parameters(), lr=learning_rate)

    # if loadFilename:
    #     optimizer.load_state_dict(checkpoint['en_opt'])

    # initialize
    print('Initializing ...')
    perplexity = []
    start_iteration = 1
    print_loss = 0

    loss_func = nn.CrossEntropyLoss()  # the target label is not one-hotted

    # training and testing
    for epoch in range(epoch):
        for iteration in tqdm(range(start_iteration, all_steps + 1)):
            training_batch = training_batches[iteration - 1]
            try:
                training_batch = torch.FloatTensor(training_batch)
            except:
                training_batch = training_batch.float()
            training_batch = training_batch.to(device)
            ans = random_answer[iteration - 1].to(device)
            output = RNNmodel(training_batch)
            output = output[0]  # select the out
            loss = loss_func(output, ans)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if iteration % 5 == 0:
                # test_output = rnn(test_x)  # (samples, time_step, input_size)
                # pred_y = torch.max(test_output, 1)[1].data.numpy()
                # accuracy = float((pred_y == test_y).astype(int).sum()) / \
                #            float(test_y.size)
                print('Epoch: {}| iteration: {}| train loss: {:.2f}'.format(
                      epoch, iteration, loss.data.cpu().numpy()))
