#!/usr/bin/python3.4

import argparse
import subprocess
import os
from shutil import copyfile, move

parser = argparse.ArgumentParser(description='Script for running tools ')
parser.add_argument('tool', choices=['GapAdj', 'PMAG', 'MGRA', 'GASTS'], type=str,
                    help='Run tool of your choice')
parser.add_argument('path', type=str, help='Path to folder with chosen parameters')

args = parser.parse_args()
tool = args.tool
path = args.path

if tool == 'PMAG':
    for test_dir in os.listdir(path):
        print(test_dir)
        old_path = str(path) + '/' + str(test_dir) + '/PMAG/'
        new_path = '~/home/hamster/tools/PMAG/'

        copyfile(old_path + 'blocks.txt', new_path)
        copyfile(old_path + 'tree.txt', new_path)

        os.chdir(new_path)
        operation = 'perl RunPMAG+.pl blocks.txt tree.txt result.txt'
        print(subprocess.call(operation, shell=True))

        move('result.txt', old_path)
        os.remove('blocks.txt')
        os.remove('tree.txt')

elif tool == 'MGRA':
    for test_dir in os.listdir(path):
        print(test_dir)
        current_path = str(path) + '/' + str(test_dir) + '/MGRA/'
        operation = '~/home/hamster/tools/MGRA/build/mgra -c ' + \
                    current_path + 'sim.cfg -f grimm - g ' + current_path + \
                    'blocks.txt -o ' + current_path + ' 2>logerror.txt >/dev/null'
        print(subprocess.call(operation, shell=True))

elif tool == 'GASTS':
    for test_dir in os.listdir(path):
        print(test_dir)
        current_path = str(path) + '/' + str(test_dir) + '/GASTS/'
        copyfile('~/home/hamster/tools/GASTS/gasts.jar', current_path)

        operation = 'java -jar ' + current_path + \
                    'gasts.jar ' + current_path + \
                    'tree.txt ' + current_path + \
                    'blocks.txt 2>logerror.txt'
        print(subprocess.call(operation, shell=True))

        os.remove(current_path + 'gasts.jar')

elif tool == 'GapAdj':
    for test_dir in os.listdir(path):
        current_path = str(path) + '/' + str(test_dir) + '/GapAdj/'
        files = os.listdir(current_path)
        trees = filter(lambda x: x.endswith('.tree'), files)
        for current_tree in trees:
            (dirName, fileName) = os.path.split(current_tree)
            (fileBaseName, fileExtension) = os.path.splitext(fileName)
            name_gen = fileBaseName + '.gap_gen'
            operation = '~/home/hamster/tools/GapAdj/GapAdj ' \
                        + current_tree + ' ' + current_path + \
                        'blocks.txt ' + current_path + name_gen \
                        + ' 25 0.6 2>logerror.txt >/dev/null'
            print(subprocess.call(operation, shell=True))






