import os

from parsers import Handler
import shutil
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures


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
        tree_file_with_tags = os.path.join(dir_path, "tree.txt")
        shutil.copyfile(tree_file_with_tags, tree_txt)
        #shutil.copyfile(self.tree_file_with_tag, tree_txt)


    def compare_dist_PMAG(self, dir_path):
        distances = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                if i == j:
                    genomes_list = [genomes[i], anc_genomes[j]]
                distances[i] = BPGscript.BreakpointGraph().DCJ_distance(BPGscript.BreakpointGraph().BPG_from_genomes(genomes_list))
        return min(distances)

    def compare_acc_PMAG(self, dir_path):
        accuracies = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                if i == j:
                    accuracies[i] = Measures.calculate_accuracy_measure(genomes[i], anc_genomes[j])
        return accuracies
