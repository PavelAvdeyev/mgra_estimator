import os

import utils.utils as utils
import utils.Genome as Genome
from parsers import Handler
import shutil
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures


class Procars_handler(Handler.Handler):

    def __init__(self):
        super(Procars_handler, self).__init__("Procars")

    '''
    Blocks file in Cars format, trees without labels, ancestors position marked with @ and
    save tree with labels for future parsing.
    '''
    def save(self, dir_path):
        procars_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(procars_dir):
            os.makedirs(procars_dir)

        blocks_txt = os.path.join(procars_dir, self.input_blocks_file)
        procars_tree_with_tag = os.path.join(procars_dir, "tree_tag.txt")
        procars_tree_txt = os.path.join(procars_dir, "tree.txt")
        tree_file_with_tag = os.path.join(dir_path, "tree.txt")
        tree_file_without_tag = os.path.join(dir_path, "bad_tree.txt")

        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        Handler.write_genomes_with_cars_in_file(blocks_txt, genomes)

        with open(tree_file_without_tag, 'r') as f:
            tree_str = f.readline().replace(';', '@;')
        with open(procars_tree_txt, 'w') as f:
            f.write(tree_str)

        shutil.copyfile(tree_file_with_tag, procars_tree_with_tag)

    def parse(self, path):
        path_dir = os.path.join(path, 'Procars', "result", 'ProCars_PQtree.txt')
        genome = Handler.parse_genome_in_procars_file(path_dir)
        return genome

    def compare_dist_procars(self, dir_path):
        distances = {}
        genome = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for j in anc_genomes:
            genomes_list = [genome, j]
            distances[j.get_name()] = BPGscript.BreakpointGraph(). \
                DCJ_distance(BPGscript.BreakpointGraph().BPG_from_genomes(genomes_list))
        return distances[max(distances)]

    def compare_acc_procars(self, dir_path):
        accuracies = {}
        genome = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for j in anc_genomes:
            print(j.get_name())
            accuracies[j.get_name()] = Measures.calculate_accuracy_measure(genome, j)
        return accuracies[min(accuracies)]



