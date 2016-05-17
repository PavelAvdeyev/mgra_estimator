import os

from parsers import Handler
import utils.Genome as Genome
import utils.utils as utils
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures
import shutil


class Rococo_handler(Handler.Handler):
    def __init__(self):
        super(Rococo_handler, self).__init__("Rococo")

    '''
    Blocks file in Rococo format,
    tree with labels used.
    '''

    def save(self, dir_path):
        rococo_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(rococo_dir):
            os.makedirs(rococo_dir)

        rococo_blocks_txt = os.path.join(rococo_dir, self.input_blocks_file)
        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        self._write_genomes(rococo_blocks_txt, genomes)

        infer_tree_with_tag = os.path.join(rococo_dir, "tree_tag.txt")
        tree_file_with_tag = os.path.join(dir_path, "tree.txt")
        shutil.copyfile(tree_file_with_tag, infer_tree_with_tag)

    def parse(self, path):
        path_dir = os.path.join(path, 'Rococo', "result")
        genomes = Handler.parse_genomes_in_rococo_file(path_dir)
        return genomes

    def _write_genomes(self, path_to_file, genomes):
        with open(path_to_file, 'w') as out:
            for genome in genomes:
                out.write("%s\n" % genome.get_name())
                for chromosome in genome:
                    for gene in chromosome:
                        if gene >= 0:
                            out.write(str(gene) + "\t" + '+\n')
                        elif gene < 0:
                            out.write(str(abs(gene)) + '\t' + '-\n')
                    if not chromosome.is_circular:
                        out.write(")\n")
                    else:
                        out.write('|\n')
                out.write("\n")

    def compare_dist_rococo(self, dir_path):
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

    def compare_acc_rococo(self, dir_path):
        accuracies = {}
        genomes = self.parse(dir_path)
        anc_genomes = Handler.parse_genomes_in_grimm_file(dir_path + '/ancestral.txt')
        for i in genomes:
            for j in anc_genomes:
                print(j.get_name())
                if i == j.get_name():
                    accuracies[i] = Measures.calculate_accuracy_measure(genomes[i], j)
        return accuracies[min(accuracies)]

