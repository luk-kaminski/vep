#!/usr/bin/env python3

import io
import numpy as np


class NamedVectors(object):

    def __init__(self, dimensions=300):
        self.data = {}
        self.dimensions = dimensions

    def add_vector(self, name, vector_data):
        if len(vector_data) != self.dimensions:
            raise ValueError(f'Expecting vector of {self.dimensions} dimensions')
        self.data[name] = vector_data

    def get_vector(self, name):
        return self.data.get(name)

    def items(self):
        return self.data.items()

    def to_matrix(self, words):
        X = np.zeros((len(words), self.dimensions))
        for (ind, word) in enumerate(words):
            vector = self.get_vector(word)
            if vector is not None:
                X[ind] = vector

        return X

    def find_synonyms(self, word_vector, threshold, word=None):
        result = []
        for (another_word, another_word_vectors) in self.data.items():
            if word is None or word != another_word:
                sim = similarity(word_vector, another_word_vectors)
                if sim > threshold:
                    result.append((another_word, sim))
        result = sorted(result, key=lambda x: -x[1])
        return result

    def find_synonyms_by_word(self, word, threshold):
        word_vector = self.data[word]
        return self.find_synonyms(word_vector, threshold, word)

    def find_similar(self, vector, how_many=3):
        top_results = [Similar() for i in range(0, how_many)]
        word_vectors = vector
        for (another_word, another_word_vectors) in self.data.items():
            sim = similarity(word_vectors, another_word_vectors)
            if sim > top_results[how_many-1].similarity:
                top_results[how_many-1] = Similar(another_word, sim)
                top_results = sorted(top_results, key=lambda x: -x.similarity)
        return top_results

    def vector_from_expression(self, expression_parts):
        vec = self.data[expression_parts[0]]
        op = ''
        for elem in expression_parts[1:]:
            if elem == ']':
                break
            elif elem == '+' or elem == '-':
                op = elem
            else:
                second_vec = self.data[elem]
                if op == '+':
                    vec = vec + second_vec
                elif op == '-':
                    vec = vec - second_vec
                else:
                    raise Exception('Wrong operation')
        return normalize(vec)


class NamedVectorsLoader(object):

    def __init__(self):
        pass

    def from_file(self, fname):
        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        named_vectors = NamedVectors()
        for line in fin:
            tokens = line.rstrip().split(' ')
            token_name = tokens[0]
            v = np.array(tokens[1:], float)
            named_vectors.add_vector(token_name, v)
        return named_vectors


class Similar(object):

    def __init__(self, name='-', similarity=0):
        self.name = name
        self.similarity = similarity


def similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def normalize(vector):
    return vector / np.linalg.norm(vector)
