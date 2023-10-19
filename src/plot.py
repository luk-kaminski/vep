#!/usr/bin/env python3

import vector_tools as vt

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PlotDraw(object):

    def __init__(self, named_vectors):
        self.named_vectors = named_vectors

    def plot_words_projections_with_professional_dimensional_reduction(self, word_groups):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        words = word_groups.words
        X = self.named_vectors.to_matrix(words)
        X_std = StandardScaler().fit_transform(X)
        pca = PCA(n_components=3)
        pca.fit(X_std)

        ax.scatter(X_std[:, 0], X_std[:, 1], X_std[:, 2])
        for (ind, word) in enumerate(words):
            ax.text(X_std[ind, 0], X_std[ind, 1], X_std[ind, 2], word, color=word_groups.get_group_color(word))
        plt.show()

    def plot_words_projections_with_dimension_selection(self, words, x_axis, y_axis, z_axis):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        x = []
        y = []
        z = []
        for word in words:
            vector = self.named_vectors.get_vector(word)
            if vector is not None:
                x.append(vector[x_axis])
                y.append(vector[y_axis])
                z.append(vector[z_axis])
                ax.text(vector[x_axis], vector[y_axis], vector[z_axis], word, color='red')

        ax.scatter(x, y, z)
        plt.show()

    def plot_similarity_distribution(self, wrd):
        if isinstance(wrd, str):
            words = [wrd]
        else:
            words = wrd

        fig, ax = plt.subplots()
        plt.yscale("log")

        for word in words:
            word_vector = self.named_vectors.get_vector(word)
            num_buckets = 201

            sim_ranges = np.linspace(-1.0, 1.0, num=num_buckets)
            counts = np.zeros(num_buckets)
            annotations = [[] for x in range(0, num_buckets)]
            for (another_word, another_word_vectors) in self.named_vectors.items():
                if not word == another_word:
                    sim = vt.similarity(word_vector, another_word_vectors)
                    index = self.similarity_to_bucket_index(sim, num_buckets)
                    counts[index] += 1
                    if len(annotations[index]) < 3:
                        annotations[index].append(another_word)
            ax.plot(sim_ranges, counts)

            if len(words) == 1:
                annotation_y_offset = 10
                annotation_x_offset = -100
                for (bi, yi) in enumerate(counts):
                    num_ann = len(annotations[bi])
                    if num_ann == 1 or num_ann == 2:
                        xi = self.bucket_index_to_similatiry(bi, num_buckets)
                        txt = ''
                        for an in annotations[bi]:
                            txt += an
                            txt += ','
                        txt = txt[:-1]

                        ax.annotate(txt, xy=(xi, yi),
                                    xycoords='data', xytext=(annotation_x_offset, annotation_y_offset),
                                    arrowprops=dict(facecolor='black', arrowstyle='->'),
                                    horizontalalignment='center', verticalalignment='bottom',
                                    textcoords='offset points')
                        annotation_y_offset += 15
                        annotation_x_offset += 15

        ax.legend(words)
        plt.show()

    def similarity_to_bucket_index(self, similarity, num_buckets):
        half = (num_buckets-1) / 2
        return int(similarity*half+half)

    def bucket_index_to_similatiry(self, bucket_index, num_buckets):
        half = (num_buckets-1) / 2
        return float(bucket_index - half)/half


class WordGroups(object):

    def __init__(self):
        self.groups = {}
        self.colors = {}
        self.words = []

    def add_group(self, name, words, color):
        if name is None or words is None or color is None:
            raise ValueError('All properties must be set!')
        self.groups[name] = words
        self.colors[name] = color
        self.words.extend(words)

    def get_group_color(self, word):
        for (group_name, words) in self.groups.items():
            if word in words:
                return self.colors[group_name]
        return 'black'
