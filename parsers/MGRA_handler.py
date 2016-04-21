import os
from parsers import Handler
import utils.utils as utils
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures


class MGRA_handler(Handler.Handler):

    def __init__(self):
        super(MGRA_handler, self).__init__("MGRA")
        #self.name_tool = "MGRA"

    def parse(self, dir_path):
        self.path_to_genomes_dir = os.path.join(dir_path, self.name_tool, "genomes")

        genomes = {}

        for genome_file, _ in utils.get_immediate_files(self.path_to_genomes_dir):
            genome = Handler.parse_genome_in_grimm_file(genome_file)
            genome.set_name(os.path.splitext(os.path.basename(genome_file))[0])
            genomes[genome.get_name()] = genome

        return genomes

    '''
    Blocks file in grimm format, configure file
    '''
    def save(self, dir_path):
        mgra_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(mgra_dir):
            os.makedirs(mgra_dir)
        blocks_txt = os.path.join(dir_path, 'blocks.txt')

        genomes = Handler.parse_genomes_in_grimm_file(blocks_txt)
        #genomes = Handler.parse_genomes_in_grimm_file(self.input_blocks_file)
        mgra_blocks_txt = os.path.join(mgra_dir, "blocks.txt")
        Handler.write_genomes_with_grimm_in_file(mgra_blocks_txt, genomes)

        tree_file_with_tag_cool =  os.path.join(dir_path, "tree.txt")
        with open(tree_file_with_tag_cool, 'r') as inp:
            tree_str = inp.readline().strip(" \t\n")
        # with open(self.tree_file_with_tag, 'r') as inp:
        #     tree_str = inp.readline().strip(" \t\n")

        config_txt = os.path.join(mgra_dir, "sim.cfg")
        with open(config_txt, 'w') as out:
            out.write("[Genomes]\n")

            for genome in genomes:
                out.write("%s\n" % genome.get_name())

            out.write("\n[Trees]\n")
            out.write("%s\n\n" % tree_str)
            out.write("[Algorithm]\n")
            out.write("stages 4\n")
            out.write("rounds 3\n")
            out.write("bruteforce 12\n\n")
            out.write("[Completion]\n")

    def parse_history_stats_file(self):
        pass

    def compare_dist_MGRA(self, dir_path):
        distances = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                if i == j:
                    genomes_list = [genomes[i], anc_genomes[j]]
                distances[i] = BPGscript.BreakpointGraph().DCJ_distance(BPGscript.BreakpointGraph().BPG_from_genomes(genomes_list))
        return min(distances)

    def compare_acc_MGRA(self, dir_path):
        accuracies = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                if i == j:
                    accuracies[i] = Measures.calculate_accuracy_measure(genomes[i], anc_genomes[j])
        return accuracies
