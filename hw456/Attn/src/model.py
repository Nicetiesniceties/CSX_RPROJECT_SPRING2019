import torch
import torch.nn as nn
import torch.nn.functional as F
from IPython import embed

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")


class RNN(nn.Module):
    def __init__(self, hidden_size, output_size, max_length, n_layers,
                 dropout):
        super(RNN, self).__init__()

        # self.rnn = nn.LSTM(
        #     input_size=max_length,
        #     hidden_size=hidden_size,
        #     num_layers=1,
        #     batch_first=True
        # )

        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout = dropout
        self.max_length = max_length

        self.gru = nn.GRU(64, self.hidden_size, self.n_layers,
                          dropout=(0 if n_layers == 1 else dropout),
                          batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x, hidden=None):  # input (batch, eq_len, input_size)
        # output (batch, seq_len, num_directions * hidden_size)
        output, hidden = self.gru(x, hidden)
        output = self.out(output[:, -1, :])
        output = self.softmax(output)
        return (output, hidden)


class AttnRNN(nn.Module):
    def __init__(self, hidden_size, output_size, max_length, n_layers=1,
                 dropout=0.1):
        super(AttnRNN, self).__init__()

        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout = dropout
        self.max_length = max_length

        # self.embedding = nn.Embedding(output_size, hidden_size)
        # self.attn = nn.Linear(hidden_size * 2, max_length)
        # self.attn_combine = nn.Linear(hidden_size * 2, hidden_size)

        self.gru = nn.GRU(64, self.hidden_size, self.n_layers,
                          dropout=(0 if self.n_layers == 1 else self.dropout),
                          batch_first=True)
        self.attn = nn.Linear(self.hidden_size, 1000)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden=None):
        output, hidden = self.gru(x, hidden)
        b_size = x.shape[0]
        output, hidden = self.gru(x, hidden)

        attn_weights = F.softmax(self.attn(hidden).view(b_size, 1, -1), dim=2)
        attn_applied = torch.bmm(attn_weights, output)

        output = self.out(attn_applied[:, -1, :])
        # output = self.softmax(output)
        output = F.softmax(output, dim=1)

        return (output, hidden, attn_weights)

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, embedding, n_layers=1,
                 dropout=0):
        super(EncoderRNN, self).__init__()
        self.n_layers = n_layers
        self.hidden_size = hidden_size
        self.embedding = embedding

        self.gru = nn.GRU(hidden_size, hidden_size, n_layers,
                          dropout=(0 if n_layers == 1 else dropout),
                          bidirectional=True)

    def forward(self, input_seq, input_lengths, hidden=None):
        embedded = self.embedding(input_seq)
        # packed = torch.nn.utils.rnn.pack_padded_sequence(embedded,
        #                                                  input_lengths)
        packed = embedded
        # output: (seq_len, batch, hidden*n_dir)
        outputs, hidden = self.gru(packed, hidden)
        # outputs, _ = torch.nn.utils.rnn.pad_packed_sequence(outputs)

        # Sum bidirectional outputs (1, batch, hidden)
        outputs = outputs[:, :, :self.hidden_size] + \
            outputs[:, :, self.hidden_size:]
        # embed()
        return outputs, hidden


class DecoderRNN(nn.Module):
    # def __init__(self, hidden_size, output_size):
    def __init__(self, embedding, hidden_size, output_size, n_layers=1,
                 dropout=0.1):
        super(DecoderRNN, self).__init__()

        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout = dropout

        self.embedding = nn.Embedding(output_size, hidden_size)
        self.embedding_dropout = nn.Dropout(dropout)
        # self.gru = nn.GRU(hidden_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, n_layers,
                          dropout=(0 if n_layers == 1 else dropout))
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    # def forward(self, input, hidden):
    def forward(self, input_seq, last_hidden, encoder_outputs):
        embedded = self.embedding(input_seq)  # .view(1, 1, -1)
        embedded = self.embedding_dropout(embedded)  # [1, 64, 512]

        embedded = F.relu(embedded)
        rnn_output, hidden = self.gru(embedded, last_hidden)

        output = self.softmax(self.out(rnn_output[0]))
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)
