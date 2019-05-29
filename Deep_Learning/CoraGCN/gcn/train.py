from model import GCN
from utils import load_dataset, accuracy

import argparse
import time
import numpy as np

import torch
import torch.optim as optim
import torch.nn.functional as F

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('-cu', '--no-cuda', action='store_true', default=False,
                    help='Enable CUDA training.')
parser.add_argument('--fastmode', action='store_true', default=False,
                    help='Validate during training pass.')
parser.add_argument('--seed', type=int, default=24, help='Random seed.')
parser.add_argument('--epochs', type=int, default=200, help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=0.01, help='Learning rate of model.')
parser.add_argument('--weight_decay', type=float, default=5e-4,
                    help='Weight decat (L2 loss on parameter).')
parser.add_argument('--hidden', type=int, default=16, help='Numbers of hidden units.')
parser.add_argument('--dropout', type=float, default=0.5,
                    help='Dropout rate (1 - keep probability).')
args = parser.parse_args()

args.cuda = not args.no_cuda and torch.cuda.is_available()
# print(args.no_cuda, args.epochs)  
np.random.RandomState(args.seed)
torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

# Load data
adj, features, labels, idx_train, idx_val, idx_test = load_dataset()

# Model and optimizer
model = GCN(n_feat=features.shape[1],
            n_hid=args.hidden,
            n_class=labels.max().item() + 1,
            dropout=args.dropout)
optimizer = optim.Adam(model.parameters(),
                        lr=args.lr, weight_decay=args.weight_decay)

if args.cuda:
    model.cuda()
    features = features.cuda()
    adj = adj.cuda()
    labels = labels.cuda()
    idx_train = idx_train.cuda()
    idx_val = idx_val.cuda()
    idx_test = idx_test.cuda()

print('labels: ', labels.shape)
def train(epoch):
    t = time.time()
    model.train()
    optimizer.zero_grad()
    output = model(features, adj)
    # print(output)
    loss_train = F.nll_loss(output[idx_train], labels[idx_train])
    acc_train = accuracy(output[idx_train], labels[idx_train])
    loss_train.backward()
    optimizer.step()

    if not args.fastmode:
        model.eval()
        output = model(features, adj)

    loss_val = F.nll_loss(output[idx_val], labels[idx_val])
    acc_val = accuracy(output[idx_val], labels[idx_val])
    print('Epoch: {:04d}'.format(epoch+1),
          'loss_train: {:.4f}'.format(loss_train),
          'acc_train: {:.4f}'.format(acc_train),
          'loss_val: {:.4f}'.format(loss_val),
          'acc_val: {:.4f}'.format(acc_val),
          'time: {:.4f}'.format(time.time()-t))

def test():
    model.eval()
    output = model(features, adj)
    loss_test = F.nll_loss(output[idx_test], labels[idx_test])
    acc_test = accuracy(output[idx_test], labels[idx_test])
    print('Test set results:',
          'loss= {:.4f}'.format(loss_test),
          'accuracy= {:.4f}'.format(acc_test))

# Train model
t_total = time.time()
for epoch in range(args.epochs):
    train(epoch)
print('Optimization Finished!')
print('Total time elapsed: {:.4f}s'.format(time.time()-t_total))

# Test
test()


                                                                       