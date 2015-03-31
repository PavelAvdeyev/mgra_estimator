import os

import Handler
import shutil
from ete2 import Tree
import utils.Genome as Genome


class GASTS_handler(Handler.Handler):
    def __init__(self):
        Handler.Handler.__init__(self, "GASTS")
        #self.name_tool = "GASTS"
        self.total_score = 0
        self.tree = None
        self.all_species = set()
        self.true_ancestor_names = {}
        self.branch_to_info = {}

    def parse(self, dir_path):
        self._parse_tree_tag(dir_path)

        path = os.path.join(dir_path, self.name_tool)

        with open(os.path.join(path, "summary_tree.txt")) as f:
            f.readline()
            f.readline()

            order_branch = list(self._parse_gasts_tree(list(f.readline().split(" "))))

            f.readline()
            f.readline()

            genomes = []
            genome = None
            chromosome = Genome.Chromosome()
            for line in f:
                line = line.strip(' \n\t')

                if line.find("#") != -1 or len(line) == 0:
                    continue

                if line.find('>') != -1:
                    if chromosome.size() != 0:
                        genome.append(chromosome)
                    if genome != None:
                        genomes.append(genome)
                    chromosome = Genome.Chromosome()
                    genome = Genome.Genome()
                    genome.set_name(line[1:])
                    continue

                for gene in line.split(' '):
                    str_gene = gene.strip(' \n\t')
                    if str_gene == '$':
                        chromosome.set_circular(False)
                        genome.append(chromosome)
                        chromosome = Genome.Chromosome()
                    elif str_gene == '@':
                        chromosome.set_circular(True)
                        genome.append(chromosome)
                        chromosome = Genome.Chromosome()
                    elif len(str_gene) != 0:
                        chromosome.append(int(str_gene))

            if chromosome.size() != 0:
                genome.append(chromosome)
            genomes.append(genome)

        result_genomes = {}

        for branch, genome in zip(order_branch, genomes):
            genome_name = self.true_ancestor_names.get(branch)
            if genome_name != None:
                genome.set_name(genome_name)
                result_genomes[genome_name] = genome

        return result_genomes

    '''
    Tree without labels, blocks file in grimm format and save tree with labels for future parsing.
    '''
    def save(self, dir_path):
        gasts_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(gasts_dir):
            os.makedirs(gasts_dir)

        blocks_txt = os.path.join(gasts_dir, self.input_blocks_file)
        gasts_tree_with_tag = os.path.join(gasts_dir, "tree_tag.txt")
        gasts_tree_txt = os.path.join(gasts_dir, "tree.txt")

        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        Handler.write_genomes_with_grimm_in_file(blocks_txt, genomes)
        shutil.copyfile(self.tree_file_with_tag, gasts_tree_with_tag)
        shutil.copyfile(self.tree_file, gasts_tree_txt)

    def _parse_tree_tag(self, dir_path):
        self.true_ancestor_names = {}
        with open(os.path.join(dir_path, self.name_tool, "tree_tag.txt")) as f:
            input_tree = Tree(f.readline().strip("\n\t"), 8)
            self.all_species = set(input_tree.get_leaf_names())
            for node in list(input_tree.traverse("preorder"))[1:]:
                if node.name not in self.all_species:
                    if not node.is_leaf():
                        left_split = list(node.children[0].get_leaf_names())
                        left_split.sort()
                        right_split = list(node.children[1].get_leaf_names())
                        right_split.sort()
                        ancestor_split = list(self.all_species.difference(set(left_split).union(set(right_split))))
                        ancestor_split.sort()

                        result = [left_split, right_split, ancestor_split]
                        result = ["".join(result[0]), "".join(result[1]), "".join(result[2])]
                        result.sort()

                        branch = " ".join(result)
                        self.true_ancestor_names[branch] = node.name

    def _parse_gasts_tree(self, dist_tree):
        order_branch = []

        self.tree, self.total_score = Tree(dist_tree[0], 5), int(dist_tree[1].strip(" \t\n"))

        for node in list(self.tree.traverse("preorder"))[1:]:
            if not node.is_leaf():
                left_split = list(node.children[0].get_leaf_names())
                left_split.sort()
                right_split = list(node.children[1].get_leaf_names())
                right_split.sort()
                ancestor_split = list(self.all_species.difference(set(left_split).union(set(right_split))))
                ancestor_split.sort()

                result = [left_split, right_split, ancestor_split]
                result = ["".join(result[0]), "".join(result[1]), "".join(result[2])]
                result.sort()

                branch = " ".join(result)

                self.branch_to_info[branch] = node.dist
                order_branch.append(branch)
            else:
                order_branch.append(node.name)

        return order_branch
