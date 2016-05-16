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
