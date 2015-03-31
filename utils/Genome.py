class Chromosome(object):
    def __init__(self):
        self.is_circ = False
        self.blocks = []
        self.position = -1

    def size(self):
        return len(self.blocks)

    def set_circular(self, is_circular):
        self.is_circ = is_circular

    def append(self, block):
        self.blocks.append(block)

    def is_circular(self):
        return self.is_circ

    def __iter__(self):
        return iter(self.blocks)


class Genome(object):
    def __init__(self, name=""):
        self.name = name
        self.chromosomes = []
        self.position = -1

    def set_name(self, name):
        self.name = name

    def append(self, chromosome):
        self.chromosomes.append(chromosome)

    def add_chromosome(self, is_circular, chromosome):
        self.chromosomes.append(Chromosome(is_circular, chromosome))

    def get_length(self):
        return len(self.chromosomes)

    def get_chromosome(self, ind):
        return self.chromosomes[ind]

    def get_name(self):
        return self.name

    def __iter__(self):
        return iter(self.chromosomes)
