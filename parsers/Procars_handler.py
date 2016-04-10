import os

import utils.utils as utils
import utils.Genome as Genome
import Handler
import shutil


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



