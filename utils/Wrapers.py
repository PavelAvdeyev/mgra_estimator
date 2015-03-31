import operator
from functools import partial

import Configure as conf
import parsers.SIMUL_handler as simul_handler
import measures.Measures as measures

import logging

logger = logging.getLogger()

def accumulation_tuple_func(first, second):
    return tuple(map(operator.add, first, second))


def accumulation_float_func(first, second):
    return first + second


def divide_tuple_func(first, count):
    TP, FN, FP = first
    return (float(TP) / count, float(FN) / count, float(FP) / count)


def divide_float_func(first, count):
    return (first / count)


def init_tuple_list_func(size):
    return [(0.0, 0.0, 0.0) for _ in range(size)]


def init_float_list_func(size):
    return [0.0 for _ in range(size)]


def process_classical_directory(tools, measure_func, init_func, accumul_func, divide_func, dir_path):
    simul_pars = simul_handler.SIMUL_handler()
    simul_genomes = simul_pars.parse(dir_path)
    different_genomes = [tool.parse(dir_path) for tool in tools]

    count = 0
    accamul = init_func(len(different_genomes))

    for name, simul_genome in simul_genomes.iteritems():
        logger.info("Work with genome " + name)
        for i in range(len(different_genomes)):
            #logger.info("Work with " + str(i) + " tool")
            accamul[i] = accumul_func(accamul[i], measure_func(simul_genome, different_genomes[i].get(name)))
        count += 1

    for i in range(len(different_genomes)):
        accamul[i] = divide_func(accamul[i], count)

    return accamul


distance_func = partial(process_classical_directory, conf.tools, measures.calculate_distance_measure,
                        init_float_list_func, accumulation_float_func, divide_float_func)


gene_content_func = partial(process_classical_directory, conf.tools, measures.calculate_gene_content_measure,
                        init_tuple_list_func, accumulation_tuple_func, divide_tuple_func)


accuracy_func = partial(process_classical_directory, conf.tools, measures.calculate_accuracy_measure,
                        init_tuple_list_func, accumulation_tuple_func, divide_tuple_func)

