
import math
import random
import numpy as np

class Brain:
    def __init__(self, layers):
        self.size = len(layers)
        self.layers = layers
        self.biases = [np.random.randn(y, 1) for y in self.layers[1:]]
        for i in self.biases:
            for j in i:
                if j[0] > 1:
                    j[0] = 1
                elif j[0] < -1:
                    j[0] = -1
        self.weights = [np.random.randn(y, x) for x, y in zip(self.layers[:-1], self.layers[1:])]
        for j in self.weights:
            for j in i:
                for k in range(j.size):
                    if j[k] > 1:
                        j[k] = 1
                    elif j[k] < -1:
                        j[k] = -1
        # print("biases")
        # print(self.biases)
        # print("weights")
        # print(self.weights)


    def feedforward(self, a):
        for w, b in zip(self.weights[:-1], self.biases[:-1]):
            a = Brain.relu(np.dot(w, a)+b)
        a = Brain.sigmoid(np.dot(self.weights[-1], a)+self.biases[-1])
        return a
    
    def crossover(self, parent):
        child = Brain(self.layers)
        for w, pw, cw in zip(self.weights, parent.weights, child.weights):
            for i in range(w.shape[0]):
                r = random.uniform(0, 1)
                if r < 0.6:
                    cut = random.randint(0, w.shape[1])
                    cw[i, :cut] = w[i, :cut]
                    cw[i, cut:] = pw[i, cut:]
                elif r < 0.8:
                    cw = w
                else:
                    cw = pw

        for b, pb, cb in zip(self.biases, parent.biases, child.biases):
            r = random.uniform(0, 1)
            if r < 0.6:
                cut = random.randint(0, b.shape[0])
                cb[:cut, 0] = b[:cut, 0]
                cb[cut:, 0] = pb[cut:, 0]
            elif r < 0.8:
                cb = b
            else:
                cb = pb

        return child

    def mutate(self, mutationRate):
        for w in self.weights:
            for i in range(w.shape[0]):
                for j in range(w.shape[1]):
                    r = random.uniform(0, 1)
                    if r < mutationRate:
                        w[i][j] += random.gauss(0, -1)
                        if w[i][j] > 1:
                            w[i][j] = 1
                        elif w[i][j] < -1:
                            w[i][j] = -1
        for b in self.biases:
            for i in range(b.size):
                    r = random.uniform(0, 1)
                    if r < mutationRate:
                        b[i][0] += random.gauss(0, -1)
                        if b[i][0] > 1:
                            b[i][0] = 1
                        elif b[i][0] < -1:
                            b[i][0] = -1


    @staticmethod
    def relu(z):
        a = np.maximum(z, 0)
        return a

    @staticmethod
    def sigmoid(z):
        a = 1.0/(1.0+np.exp(-z))
        return a
    
    @staticmethod
    def softmax(a):
        return np.exp(a)/np.sum(np.exp(a))
