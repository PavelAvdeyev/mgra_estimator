#!/usr/bin/python3.4

import argparse
import subprocess
import os
import logging
import sys
from shutil import copyfile, move, copy
import fnmatch
import csv
import time

parser = argparse.ArgumentParser(description='Script for running tools ')
parser.add_argument('tool', choices=['GapAdj', 'PMAG', 'MGRA',
                                     'GASTS', 'Procars', 'InferCarsPro', 'Rococo'], type=str,
                    help='Run tool of your choice')
parser.add_argument('path', type=str, help='Path to folder with chosen parameters')

args = parser.parse_args()
tool = args.tool
path = args.path

# Version for small tests

def main_runner(tool, path):
    for test_dir in os.listdir(path):
        print('working with ' + path + ' ' + test_dir)
        if tool == 'GapAdj':
            run_GapAdj(path, test_dir)
        if tool == 'PMAG':
            run_PMAG(path, test_dir)
        elif tool == 'MGRA':
            run_MGRA(path, test_dir)
        elif tool == 'GASTS':
            run_GASTS(path, test_dir)
        elif tool == 'Procars':
            run_procars(path, test_dir)
        elif tool == 'InferCarsPro':
            run_infercarspro(path, test_dir)
        elif tool == 'Rococo':
            run_rococo(path, test_dir)

#version for tests on whole dataset

def main_runner_all(tool, path):
    for dir in os.listdir(path):
        print('working with ' + dir)
        for test_dir in os.listdir(path + '/' + dir):
            print('working with ' + test_dir)
            if tool == 'GapAdj':
                run_GapAdj(path + '/' + dir, test_dir)
            elif tool == 'PMAG':
                run_PMAG(path + '/' + dir, test_dir)
            elif tool == 'MGRA':
                run_MGRA(path + '/' + dir, test_dir)
            elif tool == 'GASTS':
                run_GASTS(path + '/' + dir, test_dir)
            elif tool == 'Procars':
                run_procars(path + '/' + dir, test_dir)
            elif tool == 'InferCarsPro':
                run_infercarspro(path + '/' + dir, test_dir)
            elif tool == 'Rococo':
                run_rococo(path + '/' + dir, test_dir)


def run_procars(path, test_dir):
    old_path = os.path.join(path, test_dir, 'Procars', '')
    new_path = '/home/hamster/tools/procars/'
    if not os.path.isdir(old_path + 'result'):
        os.chdir(new_path)
        operation = 'python2 procars_main ' \
                    '-t '+ old_path + 'tree.txt ' \
                    '-b ' + old_path + 'blocks.txt ' \
                    '-r ' + old_path + 'result'
        print(subprocess.call(operation, shell=True))



def run_infercarspro(path, test_dir):
    old_path = os.path.join(path, test_dir, 'InferCarsPro', '')
    new_path = '/home/hamster/tools/InferCarsPro/'
    if len(fnmatch.filter(os.listdir(old_path), '*.*')) > 2:
        os.chdir(new_path)
        operation = './InferCarsPro ' + old_path + 'tree_tag.txt ' \
                    '' + old_path + 'blocks.txt'
        print(subprocess.call(operation, shell=True))
        files = os.listdir(new_path)
        infer_files = filter(lambda x: x.endswith('.txt') and x.startswith('Infer'), files)
        infer_car_files = filter(lambda x: x.endswith('.car'), files)
        for file in infer_files:
            move(file, old_path)
        for file in infer_car_files:
            move(file, old_path)


def run_PMAG(path, test_dir):
    old_path = os.path.join(path, test_dir, 'PMAG', '')
    new_path = '/home/hamster/tools/PMAG/'
    if len(fnmatch.filter(os.listdir(old_path), '*.*')) == 2:
        copy(old_path + 'blocks.txt', new_path)
        copy(old_path + 'tree.txt', new_path)
        os.chdir(new_path)
        operation = 'perl RunPMAG+.pl blocks.txt tree.txt result.txt'
        print(subprocess.call(operation, shell=True))
        move('result.txt', old_path)
        os.remove('blocks.txt')
        os.remove('tree.txt')


def run_MGRA(path, test_dir):
    current_path = os.path.join(path, test_dir, 'MGRA', '')
    if len(fnmatch.filter(os.listdir(current_path), '*.*')) > 2:
        operation = '~/tools/MGRA/build/mgra -c ' + \
                    current_path + 'sim.cfg -f grimm - g ' + current_path + \
                    'blocks.txt -o ' + current_path + ' 2>logerror.txt >/dev/null'
        print(subprocess.call(operation, shell=True))


def run_GASTS(path, test_dir):
    current_path = os.path.join(path, test_dir, 'GASTS', '')
    if len(fnmatch.filter(os.listdir(current_path), '*.*')) > 2:
        copy('/home/hamster/tools/GASTS/gasts.jar', current_path + 'gasts.jar')
        operation = 'java -jar ' + \
                    'gasts.jar ' + \
                    'tree.txt ' + \
                    'blocks.txt'
        os.chdir(current_path)
        print(subprocess.call(operation, shell=True))
        os.remove(current_path + 'gasts.jar')


def run_GapAdj(path, test_dir):
    current_path = os.path.join(path, test_dir, 'GapAdj', '')
    if len(fnmatch.filter(os.listdir(current_path), '*.*')) > 2:
        files = os.listdir(current_path)
        trees = filter(lambda x: x.endswith('.tree'), files)
        for current_tree in trees:
            dirName, fileName = os.path.split(current_tree)
            fileBaseName, fileExtension = os.path.splitext(fileName)
            name_gen = fileBaseName + '.gap_gen'
            operation = '/home/hamster/tools/GapAdj/GapAdj ' \
                        + current_tree + ' ' + dirName + \
                        '/blocks.txt ' + dirName + '/' + name_gen \
                        + ' 25 0.6'
            print(subprocess.call(operation, shell=True))


def run_rococo(path, test_dir):
    current_path = os.path.join(path, test_dir, 'Rococo', '')
    copy('/home/hamster/rococo/rococo-2.0.jar', current_path + 'rococo.jar')
    operation = 'java -jar ' + \
                'rococo.jar -m=u -p=s ' + \
                'tree_tag.txt ' + \
                'blocks.txt result'
    os.chdir(current_path)
    print(subprocess.call(operation, shell=True))
    os.remove(current_path + 'rococo.jar')

def time_check(tool, path):
    #tools = ['GapAdj', 'PMAG', 'MGRA', 'GASTS', 'Procars', 'InferCarsPro', 'Rococo']
    with open('tool_time.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['name', 'time'])
        start = time.time()
        main_runner(tool, path)
        csv_out.writerow([tool, time.time() - start])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if (len(sys.argv) < 2):
        sys.stderr.write("USAGE: tester.py <tool> <path> \n")
        sys.exit(1)

    if os.path.isfile(path):
        sys.stderr.write("<path> - is directory with strong hierarchy\n")
        sys.exit(1)

    time_check(tool, path)

    #main_runner_all(tool, path)











