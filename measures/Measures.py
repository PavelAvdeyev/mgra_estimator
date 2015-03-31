"""
    File contain functions for calculate different measures which we used for comparison:
        gene content
        accuracy
        DCJ-indel distance
        absolute difference between the tree branch lengths based on DCJ-indel distance

    Need to add for future, when MGRA start reconstructed tree:
        Common branch with input tree and reconstructed tree.
"""

import os
import subprocess

import parsers.Handler as handler
import utils.utils as utils

DCJ_DISTANCE_EXEC = "distance"


def calculate_gene_content_measure(simul_genome, real_genome):
    """
    Calculate gene content between simulation genome and real.
    Return True Positive, False Positive, True Negative
    """

    simul = set()
    real = set()

    for chr in simul_genome:
        for gene in chr:
            simul.add(abs(gene))

    for chr in real_genome:
        for gene in chr:
            real.add(abs(gene))

    pretty = simul.union(real)

    TP = (float(len(simul.intersection(real))) / len(pretty)) * 100
    FN = (float(len(simul.difference(real))) / len(pretty)) * 100
    FP = (float(len(real.difference(simul))) / len(pretty)) * 100

    return TP, FN, FP


def calculate_accuracy_measure(simul_genome, real_genome):
    """
    Calculate accuracy between simulation genome and real.
    Return True Positive, False Positive, True Negative
    """

    simul = set()
    real = set()

    def create_adjacency_set(input_set, genome):
        get_left = lambda gene: gene
        get_right = lambda gene: -gene

        for chromosome in genome:
            chr = list(chromosome)
            if chromosome.is_circular():
                input_set.add((min(get_right(chr[-1]), get_left(chr[0])), max(get_right(chr[-1]), get_left(chr[0]))))
            elif not chromosome.is_circular():
                input_set.add((min(0, get_left(chr[0])), max(0, get_left(chr[0]))))
                input_set.add((min(get_right(chr[-1]), 0), max(get_right(chr[-1]), 0)))

            for prev, next in zip(chr, chr[1:]):
                input_set.add((min(get_right(prev), get_left(next)), max(get_right(prev), get_left(next))))

    create_adjacency_set(simul, simul_genome)
    create_adjacency_set(real, real_genome)

    pretty = simul.union(real)

    #print(str(simul.difference(real)))
    #print(str(real.difference(simul)))

    TP = (float(len(simul.intersection(real))) / len(pretty)) * 100
    FN = (float(len(simul.difference(real))) / len(pretty)) * 100
    FP = (float(len(real.difference(simul))) / len(pretty)) * 100
    return TP, FN, FP


def calculate_distance_measure(first_genome, second_genome):
    """
    Calculate distance between first genome and second genome.
    Return DCJ distance and indel distance.
    """
    dcj, indel = calculate_DCJ_distance_and_indel_measure(first_genome, second_genome)
    return (dcj + indel)


def calculate_branch_length_measure(simul_first_genome, simul_second_genome, real_first_genome, real_second_genome):
    """
    Calculate differences on branch length between simulated genomes and real genomes.
    Return DCJ distance.
    """
    return abs(calculate_distance_measure(simul_first_genome, simul_second_genome)
               - calculate_distance_measure(real_first_genome, real_second_genome))


def calculate_DCJ_distance_and_indel_measure(first_genome, second_genome):
    """
    Calculate distance between first genome and second genome.
    Return DCJ distance and indel distance.
    """

    def run_code(first_file, second_file, out_file):
        if not _check_binary():
            return False

        cmdline = [DCJ_DISTANCE_EXEC, first_file, second_file, out_file]
        try:
            subprocess.check_call(cmdline)
        except subprocess.CalledProcessError as e:
            #logger.error("Some error inside native {0} module: {1}".format(OVERLAP_EXEC, e))
            return False
        return True

    first_genome_file = "first.txt"
    second_genome_file = "second.txt"
    out_f = "result.txt"

    handler.write_genome_with_grimm_in_file(first_genome_file, first_genome)
    handler.write_genome_with_grimm_in_file(second_genome_file, second_genome)

    if run_code(first_genome_file, second_genome_file, out_f):
        with open(out_f, 'r') as input:
            result = input.readline().strip(' \t\n').split(' ')
            dcj, indel = int(result[0]), int(result[1])
        os.remove(out_f)
        os.remove(first_genome_file)
        os.remove(second_genome_file)
        return dcj, indel
    else:
        os.remove(first_genome_file)
        os.remove(second_genome_file)
    return 0, 0


def _check_binary():
    """
    Checks if the native binary is available and runnable
    """
    binary = utils.which(DCJ_DISTANCE_EXEC)
    if not binary:
        # logger.error("\"{0}\" native module not found".format(OVERLAP_EXEC))
        return False

    try:
        devnull = open(os.devnull, "w")
        subprocess.check_call([DCJ_DISTANCE_EXEC, "--help"], stderr=devnull)
    except subprocess.CalledProcessError as e:
        # logger.error("Some error inside native {0} module: {1}".format(OVERLAP_EXEC, e))
        return False

    return True