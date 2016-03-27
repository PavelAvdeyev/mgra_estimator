import networkx as nx
from Handler import parse_genomes_in_grimm_file
import matplotlib.pyplot as plt


class BreakpointGraph:

    def __init__(self):
        self.BPG = nx.MultiGraph()

    def create_BPG(self, genomes):
        color = 0
        for genome in genomes:
            color += 1
            count = 0
            for i in genomes[genome]:
                self.BPG.add_edge(i[0], i[1], color=color, order=count)
                count += 1
        return self.BPG

    def add_edge(self, vertex1, vertex2, color, order):
        self.BPG.add_edge(vertex1, vertex2, color=color, order=order)

    def delete_edge(self, vertex1, vertex2):
        try:
            self.BPG.remove_edge(vertex1, vertex2)
        except:
            raise IndexError('no such edge')

    def path_finder(self, i):
        # path_finder[0] gives the number of pathes
        # path_finder[1] gives the number of cycles
        pathes = 0
        cycles = 0
        flag = True
        for j in nx.connected_components(i):
            for vertex in j:
                if nx.degree(i, vertex) == 1:
                    flag = False
            if flag:
                cycles += 1
            else:
                pathes += 1
            flag = True
        return pathes, cycles

    def DCJ_distance(self, i):
        n = len(i.edges())
        cycles = self.path_finder(i)[1]
        pathes = self.path_finder(i)[0]
        return float(n - cycles - pathes/2)

    def draw_BPG(self, first_seq, second_seq, save=False):
        # option save = True will save our graph as an image
        pos = nx.spring_layout(self.BPG)
        nx.draw_networkx_nodes(self.BPG, pos, cmap=plt.get_cmap('jet'),
                               node_color='black', node_size=50, alpha=0.8)
        nx.draw_networkx_edges(self.BPG, pos, edgelist=first_seq, width=2,
                               alpha=0.5, edge_color='r', edge_vmax=100)
        nx.draw_networkx_edges(self.BPG, pos, edgelist=second_seq, width=2,
                               alpha=0.5, edge_color='b', style='dashed')
        if save:
            plt.savefig("breakpoint_graph.png")
        return plt.show()

    def BPG_from_genomes(self, grimm_genomes_list):
        genomes_dict = {}
        genome_number = 0
        for genome in grimm_genomes_list:
            genome_number += 1
            for el in genome:
                genomes_dict[genome_number] = []
                chromosome = list(el)
                for i in range(len(chromosome)-1):
                    gene = ['h' + str(abs(chromosome[i])),
                            't' + str(abs(chromosome[i]))]
                    next_gene = ['h' + str(abs(chromosome[i+1])),
                                 't' + str(abs(chromosome[i+1]))]
                    if chromosome[i] > 0 and chromosome[i+1] > 0:
                        genomes_dict[genome_number].append([gene[1],
                                                            next_gene[0]])
                    elif chromosome[i] > 0 and chromosome[i+1] < 0:
                        genomes_dict[genome_number].append([gene[1],
                                                            next_gene[1]])
                    else:
                        genomes_dict[genome_number].append([gene[0],
                                                            next_gene[1]])
                if el.is_circular():
                    first_gene = ['h' + str(abs(chromosome[0])),
                                  't' + str(abs(chromosome[0]))]
                    last_gene = ['h' + str(abs(chromosome[-1])),
                                 't' + str(abs(chromosome[-1]))]
                    if chromosome[0] > 0 and chromosome[-1] > 0:
                        genomes_dict[genome_number].append([first_gene[0],
                                                            last_gene[1]])
                    elif chromosome[0] > 0 and chromosome[-1] < 0:
                        genomes_dict[genome_number].append([first_gene[0],
                                                            last_gene[0]])
                    else:
                        genomes_dict[genome_number].append([first_gene[1],
                                                            last_gene[0]])
        return self.create_BPG(genomes_dict)








