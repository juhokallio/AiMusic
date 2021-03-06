__author__ = 'juho'
import random
import numpy as np


class MarkovChain():

    def __init__(self, tokenized_text, order):
        self.order = order
        self.transition_matrix = {}
        self.tokens = set()
        memory = []
        for token in tokenized_text:
            self.tokens.add(token)
            memory.append(token)
            for index in range(len(memory)):
                key = tuple(memory[index:])
                if key not in self.transition_matrix:
                    self.transition_matrix[key] = 1
                else:
                    self.transition_matrix[key] += 1
            if len(memory) >= order:
                del memory[0]
        self.masses = [0] * order
        for key in self.transition_matrix:
            self.masses[len(key) - 1] += 1


    def get_order(self, order, order_keeping_p):
        while random.random() > order_keeping_p and order > 1:
            order -= 1
        return order

    def generate(self, length, g_order=None):
        text = []
        g_order = self.order if g_order is None else g_order
        while len(text) < length:
            text.append(None)
            order = self.get_order(g_order, 0.8)
            candidates = None
            mass = 0
            while order > 0 and mass == 0:
                candidates, mass = self.__generate_candidates(text, len(text) - 1, order)
                order -= 1
            goal = random.randint(1, mass)
            for token, value in candidates:
                if value >= goal:
                    text[-1] = token
                    break
            if text[-1] is None:
                print("Couldn't make it for reason or another")
        return text

    def evaluate(self, tokenized_text, order):
        p = 1
        for i, token in enumerate(tokenized_text):
            key = self.__get_key(tokenized_text, i, order)
            if key not in self.transition_matrix:
                return 0
            p *= self.transition_matrix[key]
        return p

    def log_likelihood(self, tokens):
        p = 0
        for i, token in enumerate(tokens):
            key = self.__get_key(tokens, i, len(tokens))
            if key not in self.transition_matrix:
                return -np.log(self.masses[len(key)])
            p += np.log(self.transition_matrix[key] / self.masses[len(key)])
        return p

    def __generate_candidates(self, text, index, order):
        mass = 0
        candidates = []
        for token in self.tokens:
            text[index] = token
            mass += self.evaluate(text, order)
            candidates.append((token, mass))
        return candidates, mass

    @staticmethod
    def __get_key(text, index, order):
        level = min(index, order - 1)
        return tuple(text[(index-level):index+1])
