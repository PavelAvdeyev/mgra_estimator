#!/usr/bin/python3.4

import argparse
import subprocess
import os
import logging
import sys
from shutil import copyfile, move

parser = argparse.ArgumentParser(description='Script for running tools ')
parser.add_argument('tool', choices=['GapAdj', 'PMAG', 'MGRA', 'GASTS'], type=str,
                    help='Run tool of your choice')
parser.add_argument('path', type=str, help='Path to folder with chosen parameters')

args = parser.parse_args()
tool = args.tool
path = args.path


def main_runner(tool, path):
    for test_dir in os.listdir(path):
        if tool == 'GapAdj':
            run_GapAdj(path, test_dir)
        elif tool == 'PMAG':
            run_PMAG(path, test_dir)
        elif tool == 'MGRA':
            run_MGRA(path, test_dir)
        elif tool == 'GASTS':
            run_GASTS(path, test_dir)


def run_PMAG(path, test_dir):
    old_path = os.path.join(path, test_dir, 'PMAG', '')
    new_path = '~/tools/PMAG/'
    copyfile(old_path + 'blocks.txt', new_path)
    copyfile(old_path + 'tree.txt', new_path)
    os.chdir(new_path)
    operation = 'perl RunPMAG+.pl blocks.txt tree.txt result.txt'
    print(subprocess.call(operation, shell=True))
    move('result.txt', old_path)
    os.remove('blocks.txt')
    os.remove('tree.txt')


def run_MGRA(path, test_dir):
    current_path = os.path.join(path, test_dir, 'MGRA', '')
    operation = '~/tools/MGRA/build/mgra -c ' + \
                current_path + 'sim.cfg -f grimm - g ' + current_path + \
                'blocks.txt -o ' + current_path + ' 2>logerror.txt >/dev/null'
    print(subprocess.call(operation, shell=True))


def run_GASTS(path, test_dir):
    current_path = os.path.join(path, test_dir, 'GASTS', '')
    copyfile('~/tools/GASTS/gasts.jar', current_path)
    operation = 'java -jar ' + current_path + \
                'gasts.jar ' + current_path + \
                'tree.txt ' + current_path + \
                'blocks.txt 2>logerror.txt'
    print(subprocess.call(operation, shell=True))
    os.remove(current_path + 'gasts.jar')


def run_GapAdj(path, test_dir):
    current_path = os.path.join(path, test_dir, 'GapAdj', '')
    files = os.listdir(current_path)
    trees = filter(lambda x: x.endswith('.tree'), files)
    for current_tree in trees:
        (dirName, fileName) = os.path.split(current_tree)
        (fileBaseName, fileExtension) = os.path.splitext(fileName)
        name_gen = fileBaseName + '.gap_gen'
        operation = '~/tools/GapAdj/GapAdj ' \
                    + current_tree + ' ' + current_path + \
                    'blocks.txt ' + current_path + name_gen \
                    + ' 25 0.6 2>logerror.txt >/dev/null'
        print(subprocess.call(operation, shell=True))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if (len(args) < 2):
        sys.stderr.write("USAGE: tester.py <tool> <path> \n")
        sys.exit(1)

    if os.path.isfile(path):
        sys.stderr.write("<path> - is directory with strong hierarchy\n")
        sys.exit(1)

    main_runner(tool, path)







