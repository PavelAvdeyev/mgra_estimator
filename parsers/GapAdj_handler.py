import os

import Handler
import utils.Genome as Genome
import utils.utils as utils


class GapAdj_handler(Handler.Handler):
    def __init__(self):
        super(GapAdj_handler, self).__init__("GapAdj")

    def parse(self, path):
        genomes = {}

        dir_path = os.path.join(path, self.name_tool)

        for genome_file, name_file in utils.get_immediate_files(dir_path):
            if name_file.find("gap_gen") != -1:
                names = os.path.splitext(os.path.splitext(os.path.basename(genome_file))[0])
                genome = self._parse_genome(genome_file)
                genome.set_name(names[0])
                genomes[genome.get_name()] = genome

        return genomes

    '''
    Blocks file in GapAdj format, n - 2 trees, where each internal node labeled by [T] and
    save tree with labels for future parsing.
    '''
    def save(self, dir_path):
        gapadj_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(gapadj_dir):
            os.makedirs(gapadj_dir)

        gapadj_blocks_txt = os.path.join(gapadj_dir, self.input_blocks_file)
        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        self._write_genomes(gapadj_blocks_txt, genomes)

        with open(os.path.join(dir_path, self.tree_file), 'r') as inp:
            tree_str = inp.readline().strip(" \t\n")

        with open(os.path.join(dir_path, self.tree_file_with_tag), 'r') as inp:
            tree_str_with_tag = inp.readline().strip(" \t\n")

        ancestors = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.ancestor_file))
        for ancestor in ancestors:
            target_name = ancestor.get_name()

            ind = tree_str_with_tag.find(target_name)
            count = 0
            for i in range(ind, 0, -1):
                if tree_str_with_tag[i] == ')':
                    count += 1

            target_ind = 0
            for i in range(0, len(tree_str)):
                if tree_str[i] == ')':
                    count -= 1
                if count == 0:
                    target_ind = i
                    break

            finally_str = tree_str[0:(target_ind + 1)] + "[T]" + tree_str[(target_ind + 1):]

            result_file = os.path.join(gapadj_dir, target_name + '.tree')
            with open(result_file, 'w') as out:
                out.write("%s\n" % finally_str)

    '''
    This function parse genomes files in gapadj format.
    # - comments
    > [number] - name on genome
    return genome with Genome type (see Genome class)
    '''
    def _parse_genome(self, full_name):
        genome = Genome.Genome()

        with open(full_name, 'r') as f:
            chromosome = Genome.Chromosome()

            for line in f:
                line = line.strip(' \n\t')

                if line.find("{") != -1 or len(line) == 0 or line.find("[") != -1 or line.find("]") != -1\
                        or line.find("}") != -1:
                    continue

                if line.find("name") != -1:
                    continue

                for gene in line.split(' '):
                    if len(gene) == 0 or gene == "(":
                        continue
                    elif gene == ")":
                        genome.append(chromosome)
                        chromosome = Genome.Chromosome()
                    else:
                        chromosome.append(int(gene))
        return genome

    def _write_genomes(self, path_to_file, genomes):
        with open(path_to_file, 'w') as out:
            out.write("{\n")

            for genome in genomes:
                out.write("name:%s\n[\n" % genome.get_name())
                for chromosome in genome:
                    out.write("( ")
                    for gene in chromosome:
                        out.write(str(gene) + " ")
                    out.write(")\n")
                out.write("]\n\n")

            out.write("}\n")

