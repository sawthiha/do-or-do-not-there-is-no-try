#!/usr/local/bin/env python3
import numpy as np
import pickle as pk

# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

class NeuralNet:
    def __init__(self, size_in, size_out, hidden, rate = 0.1, w_decay = 0, av = None, av_ = None, loss = None, loss_ = None):
        self.x = np.zeros((size_in, 1), dtype=np.float64)
        self.y = np.zeros((size_out, 1), dtype=np.float64)
        self.weight = []
        self.weight_ = []
        self.bias = []
        self.bias_ = []
        self.z = []
        self.activations = []
        
        idx = 0
        self.layer = len(hidden) + 1
        n = self.layer - 1
        self.weight.append(np.random.rand(hidden[idx], size_in) * np.sqrt(2 / size_in))
        self.weight_.append(np.zeros((hidden[idx], size_in)))
        self.bias.append(np.random.rand(hidden[idx], 1))
        self.bias_.append(np.zeros((hidden[idx], 1)))
        self.activations.append(np.zeros((hidden[idx], 1)))
        self.z.append(np.zeros((hidden[idx], 1)))
        idx += 1
        
        while idx < n:
            self.weight.append(np.random.rand(hidden[idx], hidden[idx - 1]) * np.sqrt(2 / hidden[idx - 1]))
            self.weight_.append(np.zeros((hidden[idx], hidden[idx - 1])))
            self.bias.append(np.random.rand(hidden[idx], 1))
            self.bias_.append(np.zeros((hidden[idx], 1)))
            self.z.append(np.zeros((hidden[idx], 1)))
            self.activations.append(np.zeros((hidden[idx], 1)))
            idx += 1
        
        self.weight.append(np.random.rand(size_out, hidden[idx - 1]) * np.sqrt(2 / hidden[idx - 1]))
        self.weight_.append(np.zeros((size_out, hidden[idx - 1])))
        self.bias.append(np.random.rand(size_out, 1))
        self.bias_.append(np.zeros((size_out, 1)))
        self.activations.append(np.zeros((size_out, 1)))
        self.z.append(np.zeros((size_out, 1)))
        
        self.rate = rate
        self.w_decay = w_decay
        
        if(hasattr(av, '__call__')):
            self.activate = av
        if(hasattr(av_, '__call__')):
            self.activate_ = av_
        if(hasattr(loss, '__call__')):
            self.cost = loss
        if(hasattr(loss_, '__call__')):
            self.cost_ = loss_
    
    def activate(self, x):
        return (1 - np.exp(-(x * 2))) / (1 + np.exp(-(x * 2)))
    
    def activate_(self, x):
        return 1 - np.square(self.activate(x))   
    
    def cost(self, y):
        return (self.y - y) ** 2
    
    def cost_(self, y):
        return (self.y - y) * 2
    
    def feed(self, x):
        self.x[:] = x.reshape((x.shape[0], 1))
        idx = 0
        n = self.layer - 1
        self.z[idx] = self.weight[idx].dot(self.x) + self.bias[idx]
        self.activations[idx] = self.activate(self.z[idx])
        idx += 1
        
        while idx < n:
            self.z[idx] = self.weight[idx].dot(self.activations[idx - 1]) + self.bias[idx]
            self.activations[idx] = self.activate(self.z[idx])
            idx += 1
        
        self.z[idx] = self.weight[idx].dot(self.activations[idx - 1]) + self.bias[idx]
        self.y = self.activate(self.z[idx])
        
    def propagate(self, y):
        y = y.reshape((y.shape[0], 1))
        idx = self.layer - 1
        i_ = self.activate_(self.z[idx]) * self.cost_(y)
        self.weight_[idx] = i_.dot(self.activations[idx - 1].T)
        self.bias_[idx] = i_
        c_ = self.weight[idx].T.dot(i_)
        idx -= 1
        
        while idx > 0:
            i_ = self.activate_(self.z[idx]) * c_
            self.weight_[idx] = i_.dot(self.activations[idx - 1].T)
            self.bias_[idx] = i_
            c_ = self.weight[idx].T.dot(i_)
            idx -= 1
        
        i_ = self.activate_(self.z[idx]) * c_
        self.weight_[idx] = i_.dot(self.x.T)
        self.bias_[idx] = i_
        
        while idx < self.layer:
            self.weight[idx] *= 1 - self.rate * self.w_decay
            self.weight[idx] -= self.rate * self.weight_[idx] 
            self.bias[idx] -= self.rate * self.bias_[idx]
            idx += 1
        
    def heetal_w(self, cur, prev, com):
        return np.random.randn(com, cur) * np.sqrt(2 / prev)
        
    def result(self):
        return self.y
    
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_(x):
    return sigmoid(x) * (1 - sigmoid(x))

def tanh(x):
    return (2 / (1 + np.exp(-2 * x))) - 1

def tanh_(x):
    return 1 - np.square(tanh(x))

def relu(x, a = 0.01):
    return x * (x > 0)

def relu_(x, a = 0.01):
    return 1 * (x > 0)
    
def soe(dif):
    return np.square(dif)

def soe_(dif):
    return 2 * dif

NEURO = None
with open('neuro.picke') as f:
    NEURO = pk.load(f)
