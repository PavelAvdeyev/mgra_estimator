#!/usr/bin/python3.4

import os 
import os.path
import sys
import logging
import utils.utils as utils

from parsers import Handler, PMAG_PLUS_handler, GapAdj_handler, MGRA_handler, Procars_handler, infercarspro_handler
from parsers.GASTS_handler import GASTS_handler


def prepare_input_files(dir_path, tools):
    ancestors_file = os.path.join(dir_path, "ancestral.txt")
    genomes_file = os.path.join(dir_path, "blocks.txt")
    tree_file = os.path.join(dir_path, "tree.txt")
    bad_tree_file = os.path.join(dir_path, "bad_tree.txt")

    if not os.path.isfile(genomes_file):
        sys.stderr.write("Directory need contain blocks.txt\n")
        sys.exit(1)

    genomes = Handler.parse_genomes_in_grimm_file(genomes_file)
    ancestors = Handler.parse_genomes_in_grimm_file(ancestors_file)


def dojob(name_directory, tools):
    for tool in tools:
        for path, name in utils.get_immediate_subdirectories(name_directory):
            for subpath, subname in utils.get_immediate_subdirectories(path):
                if tool == 'GASTS':
                    GASTS_handler().save(subpath)
                elif tool == 'MGRA':
                    MGRA_handler.MGRA_handler().save(subpath)
                elif tool == 'GapAdj':
                    GapAdj_handler.GapAdj_handler().save(subpath)
                elif tool == 'PMAG+':
                    PMAG_PLUS_handler.PMAG_PLUS_handler().save(subpath)
                elif tool == 'Procars':
                    Procars_handler.Procars_handler().save(subpath)
                elif tool == 'InferCarsPro':
                    infercarspro_handler.Infercarspro_handler().save(subpath)
                #prepare_input_files(subpath, tools)
                #prepare_ancestor(subpath)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if (len(sys.argv) < 2):
        sys.stderr.write("USAGE: walker.py <destination>\n")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        sys.stderr.write("<destination> - is directory with strong hierarchy\n")
        sys.exit(1)

    dir_path = os.path.abspath(sys.argv[1])

    tools = ['GASTS', 'PMAG+', 'MGRA', 'GapAdj', 'Procars', 'InferCarsPro']

    dojob(dir_path, tools)
    #prepare_input_files(dir_path, tools)
    #prepare_ancestor(dir_path)
