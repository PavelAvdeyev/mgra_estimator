import os
from Genome import Genome, Chromosome


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
    genome = Genome()

    with open(full_name, 'r') as f:
        chromosome = Chromosome()
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
                    chromosome = Chromosome()
                elif str_gene == '@':
                    chromosome.set_circular(True)
                    genome.append(chromosome)
                    chromosome = Chromosome()
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
        genome = Genome()
        chromosome = Chromosome()

        for line in f:
            line = line.strip(' \n\t')

            if line.find("#") != -1 or len(line) == 0:
                continue

            if line.find('>') != -1:
                if chromosome.size() != 0:
                    genome.append(chromosome)

                genomes.append(genome)

                chromosome = Chromosome()
                genome = Genome()
                genome.set_name(line[1:])
                continue

            for gene in line.split(' '):
                str_gene = gene.strip(' \n\t')
                if str_gene == '$':
                    chromosome.set_circular(False)
                    genome.append(chromosome)
                    chromosome = Chromosome()
                elif str_gene == '@':
                    chromosome.set_circular(True)
                    genome.append(chromosome)
                    chromosome = Chromosome()
                elif len(str_gene) != 0:
                    chromosome.append(int(str_gene))

        if chromosome.size() != 0:
            genome.append(chromosome)

        genomes.append(genome)

    return genomes[1:]


def parse_genome_in_procars_file(full_name):
    genome = Genome()
    with open(full_name, 'r') as f:
        chromosome = Chromosome()
        for line in f:
            line = line.strip(' \n\t')
            genome.set_name('Ancestor')

            if line.find("#") != -1 or len(line) == 0:
                continue

            line = line.strip('_Q ')
            line = line.strip(' Q_')
            chromosome = Chromosome()
            for gene in line.split(' '):
                str_gene = gene.strip(' \n\t')
                if len(str_gene) != 0:
                    chromosome.append(int(str_gene))
            chromosome.set_circular(False)
            genome.append(chromosome)
    return genome


def parse_genome_in_infercarspro_file(full_name):
    genome = Genome()
    with open(full_name, 'r') as f:
        chromosome = Chromosome()
        for line in f:
            line = line.strip(' \n\t')
            anc_name = full_name[-5]
            genome.set_name(anc_name)

            if line.find("#") != -1 or line.find('>') != -1 or len(line) == 0:
                continue

            chromosome = Chromosome()
            for gene in line.split(' '):
                str_gene = gene.strip(' \n\t')
                if str_gene == '$':
                    chromosome.set_circular(False)
                    genome.append(chromosome)
                    chromosome = Chromosome()
                elif str_gene == '@':
                    chromosome.set_circular(True)
                    genome.append(chromosome)
                    chromosome = Chromosome()
                elif len(str_gene) != 0:
                    chromosome.append(int(str_gene))

    return genome

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


def write_genomes_with_cars_in_file(path_to_file, genomes):
    """
    Write all genomes in file.
    Save in InferCARs format.
    No circular chromosomes for now
    """
    with open(path_to_file, 'w') as out:
        blocks = {}
        for genome in genomes:
            chrom_index = 1
            for chromosome in genome:
                i = 1
                for block in chromosome:
                    if abs(block) not in blocks:
                        if int(block) < 0:
                            blocks[abs(block)] = [[genome.get_name(), chrom_index,
                                                   str(i) + '-' + str(i + 98), '-']]
                        else:
                            blocks[block] = [[genome.get_name(), chrom_index,
                                              str(i) + '-' + str(i + 98), '+']]
                    else:
                        if int(block) < 0:
                            blocks[abs(block)].append([genome.get_name(), chrom_index,
                                                       str(i) + '-' + str(i + 98), '-'])
                        else:
                            blocks[block].append([genome.get_name(), chrom_index,
                                                  str(i) + '-' + str(i + 98), '+'])
                    i += 100
                chrom_index += 1
        number = 1
        for block in blocks:
            out.write(">%s\n" % str(number))
            for element in blocks[block]:
                out.write('%s.%s:%s %s\n' % (str(element[0]), str(element[1]),
                                             str(element[2]), str(element[3])))
            number += 1
            out.write('\n')