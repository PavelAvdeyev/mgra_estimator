#!/usr/bin/python

import os 
import os.path
import sys
import logging
import shutil

import utils.utils as utils
import PrepareInput.Writer as writer
import PrepareInput.Converter as converter

from parsers import Handler


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

    for tool in tools:
        tool(dir_path, tree_file, bad_tree_file, genomes, ancestors)


def dojob(name_directory, tools):
    for path, name in utils.get_immediate_subdirectories(name_directory):
        for subpath, subname in utils.get_immediate_subdirectories(path):
            prepare_input_files(subpath, tools)
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

    tools = [
        converter.save_for_MGRA,
        converter.save_for_PMAG,
        converter.save_for_GapAdj,
        converter.save_for_GASTS
    ]

    dojob(dir_path, tools)
    #prepare_input_files(dir_path, tools)
    #prepare_ancestor(dir_path)
