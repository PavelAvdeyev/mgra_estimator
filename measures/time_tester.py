#!/usr/bin/python3.4

import argparse
import subprocess
import os
from shutil import move, copy
import fnmatch
import csv
import time
import logging
import sys

parser = argparse.ArgumentParser(description='Script for measuring working time of tools')
parser.add_argument('tools', type=list, help='List of tools you want to compare')
parser.add_argument('path', type=str, help='Path to folder with chosen parameters')
parser.add_argument('result', type=str, help='Path to and name of resulting csv table')
args = parser.parse_args()
tools = args.tools
path = args.path
result_path = args.result

class tester():
    def run_procars(self, path, test_dir):
        old_path = os.path.join(path, test_dir, 'Procars', '')
        new_path = '/home/hamster/tools/procars/'
        if not os.path.isdir(old_path + 'result'):
            os.chdir(new_path)
            operation = 'python2 procars_main ' \
                    '-t '+ old_path + 'tree.txt ' \
                    '-b ' + old_path + 'blocks.txt ' \
                    '-r ' + old_path + 'result'
            print(subprocess.call(operation, shell=True))



    def run_infercarspro(self, path, test_dir):
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
                move(file, old_path + '/time')
            for file in infer_car_files:
                move(file, old_path + '/time')


    def run_PMAG(self, path, test_dir):
        old_path = os.path.join(path, test_dir, 'PMAG', '')
        new_path = '/home/hamster/tools/PMAG/'
        if len(fnmatch.filter(os.listdir(old_path), '*.*')) > 1:
            copy(old_path + 'blocks.txt', new_path)
            copy(old_path + 'tree.txt', new_path)
            os.chdir(new_path)
            operation = 'perl RunPMAG+.pl blocks.txt tree.txt result.txt'
            print(subprocess.call(operation, shell=True))
            move('result.txt', old_path + '/time')
            os.remove('blocks.txt')
            os.remove('tree.txt')


    def run_MGRA(self, path, test_dir):
        current_path = os.path.join(path, test_dir, 'MGRA', '')
        if len(fnmatch.filter(os.listdir(current_path), '*.*')) > 2:
            operation = '~/tools/MGRA/build/mgra -c ' + \
                    current_path + 'sim.cfg -f grimm - g ' + current_path + \
                    'blocks.txt -o ' + current_path + ' 2>logerror.txt >/dev/null'
            print(subprocess.call(operation, shell=True))


    def run_GASTS(self, path, test_dir):
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


    def run_GapAdj(self, path, test_dir):
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


    def run_rococo(self, path, test_dir):
        current_path = os.path.join(path, test_dir, 'Rococo', '')
        copy('/home/hamster/rococo/rococo-2.0.jar', current_path + 'rococo.jar')
        operation = 'java -jar ' + \
                'rococo.jar -m=u -p=s ' + \
                'tree_tag.txt ' + \
                'blocks.txt result'
        os.chdir(current_path)
        print(subprocess.call(operation, shell=True))
        os.remove(current_path + 'rococo.jar')

    def time_check(self, tool, path, test_dir):
            start = time.time()
            print('working with ' + test_dir)
            if tool == 'GapAdj':
                self.run_GapAdj(path, test_dir)
            elif tool == 'PMAG':
                self.run_PMAG(path, test_dir)
            elif tool == 'MGRA':
                self.run_MGRA(path, test_dir)
            elif tool == 'GASTS':
                self.run_GASTS(path, test_dir)
            elif tool == 'Procars':
                self.run_procars(path, test_dir)
            elif tool == 'InferCarsPro':
                self.run_infercarspro(path, test_dir)
            elif tool == 'Rococo':
                self.run_rococo(path, test_dir)
            times.append(time.time() - start)


def test_time(tools, path, result_path):
    with open(result_path, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['name', 'time'])
        for tool in tools:
            times = []
            for i in [1,2,3,4,5,6,7,8,9,10]:
                tester().time_check(tool, path, '1')
            mean_time = sum(times)/len(times)
            csv_out.writerow([tool, mean_time])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if (len(sys.argv) < 2):
        sys.stderr.write("USAGE: time_tester.py <tool> <path> <result> \n")
        sys.exit(1)

    if os.path.isfile(path):
        sys.stderr.write("<path> - is directory with strong hierarchy\n")
        sys.exit(1)

    test_time(tools, path, result_path)