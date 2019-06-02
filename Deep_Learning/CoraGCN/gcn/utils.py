import numpy as np
import torch
import scipy.sparse as sp
import os

DIRNAME = os.path.dirname(os.path.realpath(__file__))

def encode_onehot(labels):
    '''Encode label to one-hot vector'''
    classes = set(labels)
    # print(labels)
    classes_dict = {j: np.identity(len(classes))[i] for i, j in 
                    enumerate(classes)}
    labels_onehot = np.array(list(map(classes_dict.get, labels)), 
                    dtype=np.int32)
    return labels_onehot


def normalize(m):
    '''Row-normalize sparse matrix'''
    rowsum = np.array(m.sum(1))
    r = np.power(rowsum, -1).flatten()
    r[np.isnan(r) | np.isinf(r)] = 0.
    r_diag = sp.diags(r)
    return r_diag.dot(m)


def sparse_mx_to_torch_sparse_tensor(spm):
    '''Convert sparse matrix to a torch sparse tensor'''
    spm = spm.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((spm.row, spm.col)).astype(np.int64))
    value = torch.from_numpy(spm.data)
    shape = torch.Size(spm.shape)
    return torch.sparse.FloatTensor(indices, value, shape)


def load_dataset(path=DIRNAME+'/../cora/', dataset='cora'):
    '''Load dataset and process'''
    print('Loading {} dataset...'.format(dataset))

    idx_features_labels = np.genfromtxt('{}{}.content'.format(path, dataset),
                                        dtype=np.dtype(str))
    '''
    array([['31336', '0', '0', ..., '0', '0', 'Neural_Networks'],
       ...,
       ['24043', '0', '0', ..., '0', '0', 'Neural_Networks']], dtype='<U22')
    '''
    idx = np.array(idx_features_labels[:, 0], dtype=np.int32)
    features = sp.csr_matrix(idx_features_labels[:, 1:-1], dtype=np.float32)
    labels = encode_onehot(idx_features_labels[:, -1])
    print(labels.shape)
    # build graph
    idx_map = {j: i for i, j in enumerate(idx)}
    edges_unordered = np.genfromtxt('{}{}.cites'.format(path, dataset), 
                                    dtype=np.int32)
    edges = np.array(list(map(idx_map.get, edges_unordered.flatten())),
                    dtype=np.int32).reshape(edges_unordered.shape)
    adj = sp.coo_matrix((np.ones(edges.shape[0]), (edges[:, 0], edges[:, 1])),
                        shape=(labels.shape[0], labels.shape[0]),
                        dtype=np.float32)

    # build symmetric adjacency matrix
    adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)

    features = normalize(features)
    adj = normalize(adj + sp.eye(adj.shape[0]))

    # train, validate, test index split
    idx_train = torch.LongTensor(range(199))
    idx_val = torch.LongTensor(range(200, 500))
    idx_test = torch.LongTensor(range(500, 1500))

    features = torch.FloatTensor(np.array(features.todense()))
    labels = torch.LongTensor(np.where(labels)[1]) # union of y coordinate of 1
    adj = sparse_mx_to_torch_sparse_tensor(adj)
                    
    return adj, features, labels, idx_train, idx_val, idx_test

def accuracy(output, labels):
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double().sum()
    return correct / len(labels)

# load_dataset()