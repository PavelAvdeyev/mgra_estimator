import os
import sys

import Handler
import utils.utils as utils

class SIMUL_handler(Handler.Handler):
    def __init__(self):
        super(SIMUL_handler, self).__init__("simul")
        #self.name_tool = "simul"

    def parse(self, dir_path):
        genomes = {}
        path = os.path.join(dir_path, self.name_tool)

        for path_to_file, _ in utils.get_immediate_files(path):
            genome = Handler.parse_genome_in_grimm_file(path_to_file)
            genomes[genome.get_name()] = genome

        return genomes

    def save(self, dir_path):
        ancestors_file = os.path.join(dir_path, self.ancestor_file)

        if not os.path.isfile(ancestors_file):
            sys.stderr.write("Directory need contain ancestral.txt\n")
            sys.exit(1)

        genomes = Handler.parse_genomes_in_grimm_file(ancestors_file)
        simul_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(simul_dir):
            os.makedirs(simul_dir)

        Handler.write_genomes_with_grimm_by_name(simul_dir, genomes, ".sim_gen")
