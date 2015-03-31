import os
import utils.Genome as Genome


class Handler(object):
    def __init__(self, name_tool):
        self.name_tool = name_tool
        self.tree_file_with_tag = "tree.txt"
        self.tree_file = "bad_tree.txt"
        self.input_blocks_file = "blocks.txt"
        self.ancestor_file = "ancestral.txt"

    def get_name_tool(self):
        return self.name_tool


def parse_genome_in_grimm_file(full_name):
    """
    This function parse genomes files in grimm format.
    # - comments
    > [number] - name on genome
    return genome have genome type (see Genome class)
    """
    genome = Genome.Genome()

    with open(full_name, 'r') as f:
        chromosome = Genome.Chromosome()
        for line in f:
            line = line.strip(' \n\t')

            if line.find("#") != -1 or len(line) == 0:
                continue

            if line.find('>') != -1:
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
    return genome


def parse_genomes_in_grimm_file(full_name):
    """
    This function parse genomes files in grimm format.
    # - comments
    > [number] - name on genome
    return [genomes] where genome have genome type (see Genome class)
    """
    genomes = []

    with open(full_name, 'r') as f:
        genome = Genome.Genome()
        chromosome = Genome.Chromosome()

        for line in f:
            line = line.strip(' \n\t')

            if line.find("#") != -1 or len(line) == 0:
                continue

            if line.find('>') != -1:
                if chromosome.size() != 0:
                    genome.append(chromosome)

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

    return genomes[1:]


def write_genomes_with_grimm_by_name(dir_path, genomes, type):
    """
    Write genomes in files. Each file have name according genome name.
    Save in grimm format.
    """
    for genome in genomes:
        name_genome_file = os.path.join(dir_path, genome.get_name() + type)

        with open(name_genome_file, 'w') as out:
            out.write(">%s\n" % genome.get_name())
            for chromosome in genome:
                for gene in chromosome:
                    out.write(str(gene) + " ")

                if chromosome.is_circular():
                    out.write(" @\n")
                else:
                    out.write(" $\n")


def write_genomes_with_grimm_in_file(path_to_file, genomes):
    """
    Write all genomes in file.
    Save in grimm format.
    """
    with open(path_to_file, 'w') as out:
        for genome in genomes:
            out.write(">%s\n" % genome.get_name())
            for chromosome in genome:
                for gene in chromosome:
                    out.write(str(gene) + " ")

                if chromosome.is_circular():
                    out.write(" @\n")
                else:
                    out.write(" $\n")


def write_genome_with_grimm_in_file(path_to_file, genome):
    """
    Write genome in file in grimm format.
    """
    with open(path_to_file, 'w') as out:
        if len(genome.get_name()) != 0:
            out.write(">%s\n" % genome.get_name())

        for chromosome in genome:
            for gene in chromosome:
                out.write(str(gene) + " ")

            if chromosome.is_circular():
                out.write(" @\n")
            else:
                out.write(" $\n")
