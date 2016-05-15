import os

import utils.utils as utils
from utils.Genome import Genome, Chromosome
from parsers import Handler
import shutil
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures


class Infercarspro_handler(Handler.Handler):

    def __init__(self):
        super(Infercarspro_handler, self).__init__("InferCarsPro")

    '''
    Blocks file in GRIMM format with given number of chromosomes
    in genomes, trees without labels and save tree with labels
    for future parsing.
    '''

    def save(self, dir_path):
        infercarspro_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(infercarspro_dir):
            os.makedirs(infercarspro_dir)

        blocks_txt = os.path.join(infercarspro_dir, self.input_blocks_file)
        infer_tree_with_tag = os.path.join(infercarspro_dir, "tree_tag.txt")
        infer_tree_txt = os.path.join(infercarspro_dir, "tree.txt")
        tree_file_with_tag = os.path.join(dir_path, "tree.txt")
        tree_file_without_tag = os.path.join(dir_path, "bad_tree.txt")

        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        with open(blocks_txt, 'w') as f:
            for genome in genomes:
                f.write(">%s %d\n" % (genome.get_name(), genome.get_length()))
                for chromosome in genome:
                    for gene in chromosome:
                        f.write(str(gene) + " ")

                    if chromosome.is_circular():
                        f.write(" @\n")
                    else:
                        f.write(" $\n")

        shutil.copyfile(tree_file_with_tag, infer_tree_with_tag)


    def parse(self, path):
        current_path = os.path.join(path, 'InferCarsPro')
        files = os.listdir(current_path)
        ancestors = filter(lambda x: x.startswith('Ancestor'), files)
        genomes = {}
        for ancestor in ancestors:
            full_path = os.path.join(current_path, ancestor)
            genome = Handler.parse_genome_in_infercarspro_file(full_path)
            genomes[genome] = genome.get_name()
        return genomes

    def compare_dist_Infercarspro(self, dir_path):
        distances = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                if i == j.get_name():
                    genomes_list = [genomes[i], j]
            distances[i] = BPGscript.BreakpointGraph(). \
                DCJ_distance(BPGscript.BreakpointGraph().BPG_from_genomes(genomes_list))
        return distances[max(distances)]

    def compare_acc_Infercarspro(self, dir_path):
        accuracies = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                print(j.get_name())
                if i == j.get_name():
                    accuracies[i] = Measures.calculate_accuracy_measure(genomes[i], j)
        return accuracies[min(accuracies)]