#!/usr/local/bin/env python3
import numpy as np

# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

# Two layer Neural Net
class NeuralNet:
    def __init__(self, size_in, size_out, n, rate = 0.1, w_decay = 0, av = None, av_ = None, loss = None, loss_ = None):
        self.input = np.zeros((size_in, 1), dtype=np.float64)
        self.output = np.zeros((size_out, 1), dtype=np.float64)
        self.weight = [None, None, None]
        self.bias = [None, None, None]
        self.layer = [None, None]
        self.z = [None, None, None]
        self.weight_ = [None, None, None]
        self.bias_ = [None, None, None]
        self.weight[0] = np.random.rand(n, size_in) * np.sqrt(2 / size_in)
        self.weight[1] = np.random.rand(n, n) * np.sqrt(2 / n)
        self.weight[2] = np.random.rand(size_out, n) * np.sqrt( 2 / n)
        self.bias[0] = np.random.rand(n, 1)
        self.bias[1] = np.random.rand(n, 1)
        self.bias[2] = np.random.rand(size_out, 1)
        self.layer[0] = np.zeros((n, 1), dtype=np.float64)
        self.layer[1] = np.zeros((n, 1), dtype=np.float64)
        self.z[0] = np.zeros((n, 1), dtype=np.float64)
        self.z[1] = np.zeros((n, 1), dtype=np.float64)
        self.z[2] = np.zeros((size_out, 1), dtype=np.float64)
        self.weight_[0] = np.zeros((n, size_in), dtype=np.float64)
        self.weight_[1] = np.zeros((n, n), dtype=np.float64)
        self.weight_[2] = np.zeros((size_out, n), dtype=np.float64)
        self.bias_[0] = np.zeros((n, 1), dtype=np.float64)
        self.bias_[1] = np.zeros((n, 1), dtype=np.float64)
        self.bias_[2] = np.zeros((size_out, 1), dtype=np.float64)
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
        return (self.output - y) ** 2
    
    def cost_(self, y):
        return (self.output - y) * 2
    
    def feed(self, x):
        self.input = x.T
        self.z[0] = self.weight[0].dot(self.input) + self.bias[0]
        self.layer[0] = self.activate(self.z[0])
        self.z[1] = self.weight[1].dot(self.layer[0]) + self.bias[1]
        self.layer[1] = self.activate(self.z[1])
        self.z[2] = self.weight[2].dot(self.layer[1]) + self.bias[2]
        self.output = self.activate(self.z[2])
        
    def propagate(self, y):
        i_ = self.activate_(self.z[2]) * self.cost_(y)
        self.weight_[2] = i_.dot(self.layer[1].T)
        self.bias_[2] = i_
        c_ = self.weight[2].T.dot(i_)
        
        i_ = self.activate_(self.z[1]) * c_
        self.weight_[1] = i_.dot(self.layer[0].T)
        self.bias_[1] = i_
        c_ = self.weight[1].T.dot(i_)
        
        i_ = self.activate_(self.z[0]) * c_
        self.weight_[0] = i_.dot(self.input.T)
        self.bias_[0] = i_
        
        for i in range(0, 3, 1):
            self.weight[i] *= 1 - self.rate * self.w_decay
            self.weight[i] -= self.rate * self.weight_[i] 
            self.bias[i] -= self.rate * self.bias_[i]
        
    def result(self):
        return self.output

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