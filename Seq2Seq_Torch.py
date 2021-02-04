# -*- coding: utf-8 -*-
"""Seq2Seq-Torch
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/18-pjFO8qYHOIqbb3aSReNpAbqZHCzLXq
"""

# code by Tae Hwan Jung(Jeff Jung) @graykode, modify by wmathor
import torch
import numpy as np
import torch.nn as nn
import torch.utils.data as Data

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# S: Symbol that shows starting of decoding input
# E: Symbol that shows starting of decoding output
# ?: Symbol that will fill in blank sequence if current batch data size is short than n_step

letter = [c for c in 'SE?abcdefghijklmnopqrstuvwxyz']
letter2idx = {n: i for i, n in enumerate(letter)}

seq_data = [['man', 'women'], ['black', 'white'], ['king', 'queen'], ['girl', 'boy'], ['up', 'down'], ['high', 'low']]

# Seq2Seq Parameter
n_step = max([max(len(i), len(j)) for i, j in seq_data]) # max_len(=5)
n_hidden = 128
n_class = len(letter2idx) # classfication problem
batch_size = 3

def make_data(seq_data):
    enc_input_all, dec_input_all, dec_output_all = [], [], []

    for seq in seq_data:
        for i in range(2):
            seq[i] = seq[i] + '?' * (n_step - len(seq[i])) # 'man??', 'women'

        enc_input = [letter2idx[n] for n in (seq[0] + 'E')] # ['m', 'a', 'n', '?', '?', 'E']
        dec_input = [letter2idx[n] for n in ('S' + seq[1])] # ['S', 'w', 'o', 'm', 'e', 'n']
        dec_output = [letter2idx[n] for n in (seq[1] + 'E')] # ['w', 'o', 'm', 'e', 'n', 'E']

        enc_input_all.append(np.eye(n_class)[enc_input])
        dec_input_all.append(np.eye(n_class)[dec_input])
        dec_output_all.append(dec_output) # not one-hot

    # make tensor
    return torch.Tensor(enc_input_all), torch.Tensor(dec_input_all), torch.LongTensor(dec_output_all)

'''
enc_input_all: [6, n_step+1 (because of 'E'), n_class]
dec_input_all: [6, n_step+1 (because of 'S'), n_class]
dec_output_all: [6, n_step+1 (because of 'E')]
'''
enc_input_all, dec_input_all, dec_output_all = make_data(seq_data)

class TranslateDataSet(Data.Dataset):
    def __init__(self, enc_input_all, dec_input_all, dec_output_all):
        self.enc_input_all = enc_input_all
        self.dec_input_all = dec_input_all
        self.dec_output_all = dec_output_all
    
    def __len__(self): # return dataset size
        return len(self.enc_input_all)
    
    def __getitem__(self, idx):
        return self.enc_input_all[idx], self.dec_input_all[idx], self.dec_output_all[idx]

loader = Data.DataLoader(TranslateDataSet(enc_input_all, dec_input_all, dec_output_all), batch_size, True)

# Model
class Seq2Seq(nn.Module):
    def __init__(self):
        super(Seq2Seq, self).__init__()
        self.encoder = nn.RNN(input_size=n_class, hidden_size=n_hidden, dropout=0.5) # encoder
        self.decoder = nn.RNN(input_size=n_class, hidden_size=n_hidden, dropout=0.5) # decoder
        self.fc = nn.Linear(n_hidden, n_class)

    def forward(self, enc_input, enc_hidden, dec_input):
        # enc_input(=input_batch): [batch_size, n_step+1, n_class]
        # dec_inpu(=output_batch): [batch_size, n_step+1, n_class]
        enc_input = enc_input.transpose(0, 1) # enc_input: [n_step+1, batch_size, n_class]
        dec_input = dec_input.transpose(0, 1) # dec_input: [n_step+1, batch_size, n_class]

        # h_t : [num_layers(=1) * num_directions(=1), batch_size, n_hidden]
        _, h_t = self.encoder(enc_input, enc_hidden)
        # outputs : [n_step+1, batch_size, num_directions(=1) * n_hidden(=128)]
        outputs, _ = self.decoder(dec_input, h_t)

        model = self.fc(outputs) # model : [n_step+1, batch_size, n_class]
        return model

model = Seq2Seq().to(device)
criterion = nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
