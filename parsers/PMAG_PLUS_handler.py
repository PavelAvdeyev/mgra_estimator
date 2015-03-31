import os

import Handler
import shutil


class PMAG_PLUS_handler(Handler.Handler):
    def __init__(self):
        super(PMAG_PLUS_handler, self).__init__("PMAG")
        #self.name_tool = "PMAG"

    def parse(self, path):
        genomes = {}

        path_dir = os.path.join(path, self.name_tool, "result.txt")
        temp_genomes = Handler.parse_genomes_in_grimm_file(path_dir)

        for genome in temp_genomes:
            genomes[genome.get_name()] = genome

        return genomes

    '''
    Blocks file in grimm format, tree with labeled ancestors
    '''
    def save(self, dir_path):
        pmag_plus_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(pmag_plus_dir):
            os.makedirs(pmag_plus_dir)

        pmag_plus_blocks_txt = os.path.join(pmag_plus_dir, self.input_blocks_file)
        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        Handler.write_genomes_with_grimm_in_file(pmag_plus_blocks_txt, genomes)

        tree_txt = os.path.join(pmag_plus_dir, "tree.txt")
        shutil.copyfile(self.tree_file_with_tag, tree_txt)

