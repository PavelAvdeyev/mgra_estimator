import os

import utils.utils as utils
from utils.Genome import Genome, Chromosome
import Handler
import shutil


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
                f.write(">%s %d\n" % (Genome().get_name(), Genome().get_length()))
                for chromosome in genome:
                    for gene in chromosome:
                        f.write(str(gene) + " ")

                    if chromosome.is_circular():
                        f.write(" @\n")
                    else:
                        f.write(" $\n")

        shutil.copyfile(tree_file_with_tag, infer_tree_with_tag)