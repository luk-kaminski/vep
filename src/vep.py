#!/usr/bin/env python3

import vector_tools as vt
from plot import PlotDraw
from plot import WordGroups

import sys
import time
import traceback


def contains_expression(text_array):
    return text_array[0] == '[' and ']' in text_array

def help(command):
    if command == 'comp' or command == 'help':
        print('comp [word1] [word2] -> Print similarity of [word1] and [word2]')
        print('\t Example: comp queen king')
    if command == 'syn' or command == 'help':
        print('syn [word] [min_similarity(0.6 by default)] -> list synonyms for [word] with minimal similarity of [min_similarity]')
        print('\t Example: syn queen 0.7')
        print('syn [expression] [min_similarity(0.6 by default)] -> list synonyms for [expression] with minimal similarity of [min_similarity]')
        print('\t Example: syn [ queen - woman ] 0.7')
    if command == 'plot' or command == 'help':
        print('plot [word] -> plot similarity distribution of [word], with most/least similar words annotated')
        print('\t Example: plot queen')
        print('plot [word1,word2...] -> plot similarity distribution of a list of words')
        print('\t Example: plot queen,king,throne')
    if command == 'points' or command == 'help':
        print('points -> plot selected vectors after dimension reduction')
    if command == 'help':
        print('help -> prints this help')
    if command == 'exit' or command == 'help':
        print('exit -> exit the program')



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please provide vector data file as the first argument')
        exit()
    file_name = sys.argv[1]
    try:
        start_time = time.time()
        data = vt.NamedVectorsLoader().from_file(file_name)
        stop_time = time.time()
        print('Loading vectors took ', (stop_time - start_time), ' seconds')
    except:
        print('Something is wrong with your vector data file...')
        traceback.print_exc()
        exit()

    command = None

    while command == None or command[0] != 'exit':
        print('='*15)
        command = input('Enter command : ').split(' ')
        print('='*15)

        if command[0] == 'syn':
            try:
                limit = '0.6' if len(command) < 3 or command[-1] == ']' else command[-1]
                if contains_expression(command[1:]):
                    vec = data.vector_from_expression(command[2:command.index(']')])
                else:
                    vec = data.get_vector(command[1])
                result = data.find_synonyms(vec, float(limit))
                for (k, v) in result:
                    print("{0} : {1:.2f}".format(k, v))
            except:
                print('Command mis-used, valid usage:')
                help(command[0])
        elif command[0] == 'comp':
            try:
                if '[' not in command:
                    word1 = command[1]
                    vec1 = data.get_vector(word1)
                    word2 = command[2]
                    vec2 = data.get_vector(word2)
                else:
                    close_bracket_index = command.index(']')
                    vec1 = data.vector_from_expression(command[2:close_bracket_index])
                    exp2 = command[close_bracket_index+1:]
                    if contains_expression(exp2):
                        vec2 = data.vector_from_expression(exp2[1: exp2.index(']')])
                    else:
                        vec2 = data.get_vector(exp2[0])
                similarity = vt.similarity(vec1, vec2)
                print("Similarity : {0:.2f}".format(similarity))
            except:
                print('Command mis-used, valid usage:')
                help(command[0])
        elif command[0] == 'points':
            try:
                plotter = PlotDraw(data)
                # TODO: allow easy change of those hardcoded values
                word_groups = WordGroups()
                word_groups.add_group('sports', ['basketball', 'volleyball', 'baseball', 'football', 'soccer', 'surfing'], 'red')
                word_groups.add_group('computers', ['computer', 'laptop', 'notebook', 'PC', 'mainframe', 'calculator'], 'blue')
                word_groups.add_group('aristocracy', ['king', 'queen', 'prince', 'princess', 'duke', 'monarch'], 'orange')
                word_groups.add_group('nationalities', ['Nigerian', 'Japanese', 'German', 'Polish', 'Czech', 'Ukrainian'], 'green')

                plotter.plot_words_projections_with_professional_dimensional_reduction(word_groups)
            except:
                print('Command mis-used, valid usage:')
                help(command[0])
        elif command[0] == 'plot':
            try:
                plotter = PlotDraw(data)
                word = command[1]
                if ',' in word:
                    plotter.plot_similarity_distribution(word.split(','))
                else:
                    plotter.plot_similarity_distribution(word)
            except:
                print('Command mis-used, valid usage:')
                help(command[0])
        elif command[0] == 'help':
            print('Valid commands:')
            help(command[0])






