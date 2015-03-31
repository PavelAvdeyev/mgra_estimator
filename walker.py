#!/usr/bin/python

import os
import re
import sys
import logging
from functools import partial

import Configure as conf

import parsers.GASTS_handler as gasts_handler

import graphics_drawer.bar_chart as bar_chart
import measures.Measures as measures
import utils.utils as utils
import utils.Wrapers as wrap


def dojob(number_tools, init_func, accumul_func, divide_func, dir_path, filter_func, procces_directory_func):
    answer = {}

    for path, name in utils.get_immediate_subdirectories(dir_path):
        logging.info("Worked with " + name + " dataset")
        expr = re.match('(\d+)_(\d+)_(\d+)_(\d+)', name)
        params = (int(expr.group(1)), int(expr.group(2)), int(expr.group(3)), int(expr.group(4)))

        if filter_func(params):
            accamul = init_func(number_tools)
            count = 0

            for subpath, subname in utils.get_immediate_subdirectories(path):
                logging.info("Process next example with number " + subname + " dataset")
                current = procces_directory_func(subpath)
                count += 1
                for i in range(number_tools):
                    accamul[i] = accumul_func(accamul[i], current[i])

            for i in range(number_tools):
                accamul[i] = divide_func(accamul[i], count)
            answer[params] = accamul
    return answer


float_dojob = partial(dojob, len(conf.tools), wrap.init_float_list_func, wrap.accumulation_float_func,
                          wrap.divide_float_func)

tuple_dojob = partial(dojob, len(conf.tools), wrap.init_tuple_list_func, wrap.accumulation_tuple_func,
                          wrap.divide_tuple_func)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if (len(sys.argv) < 3):
        sys.stderr.write("USAGE: walker.py <destination> <output_dir>\n")
        sys.stderr.write("destination - is directory with strong hierarchy created by PrepareInput\n")
        sys.exit(1)


    dir_path = os.path.abspath(sys.argv[1])
    output_dir = os.path.join(sys.argv[2])

    params_files = [6, 9, 12, 15]

    for index in params_files:
        print(index)

        distance_file = os.path.join(output_dir, "distance" + str(index) + ".pdf")
        answer = float_dojob(dir_path, partial(conf.filter_genomes_by_species, 12), wrap.distance_func)
        bar_chart.draw_clustered_histogram(distance_file, answer)

        accuracy_file = os.path.join(output_dir, "accuracy" + str(index) + ".pdf")
        answer = tuple_dojob(dir_path, partial(conf.filter_genomes_by_species, index), wrap.accuracy_func)
        name_labels, vals, min_y = bar_chart.prepare_unique_datasets(conf.tools, answer)
        bar_chart.draw_clustered_stacked_histigram(accuracy_file, name_labels, vals, min_y, "Accuracy content", len(conf.tools))

    '''
    for key, res in answer.iteritems():
        _, genes, rear, _ = key
        name = "(" + str(5 * genes) + "," + str(rear) + ")"
        print("Dataset: " + name)
        print("MGRA")
        print(res[0])
        print("PMAG+")
        print(res[1])
        print("GapAdj")
        print(res[2])
        print("GASTS")
        print(res[3])
    '''

    #distance_file = os.path.join(output_dir, "distance9.pdf")
    #bar_chart.draw_clustered_histogram(distance_file, answer)

    '''answer = dojob(dir_path, len(conf.tools),
                   partial(conf.filter_genomes_by_species, 9),
                   partial(process_classical_directory_with_errors, conf.tools, measures.calculate_accuracy_measure))

    output_dir = os.path.join(sys.argv[2])
    accuracy_file = os.path.join(output_dir, "accuracy9.pdf")
    name_labels, vals, min_y = bar_chart.prepare_unique_datasets(conf.tools, answer)
    bar_chart.draw_clustered_stacked_histigram(accuracy_file, name_labels, vals, min_y, "Accuracy content", len(conf.tools))
    '''




