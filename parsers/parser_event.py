import networkx as nx

def parse(file_name):
    event = {}
    with open(file_name) as f:
        for line in f:
            k2 = line.split(':')[0].split(' ')
            k1 = str(k2[0]) + ' ' + str(k2[2])
            info = line.split(':')[1].split(', #')
            summary = [info[0].split(' ')[2], info[1].split(' ')[2],
                    info[2].split(' ')[2], info[3].split(' ')[2]]
            event[k1] = summary
    return event

def count_overall_distance(file_name, start_genome, end_genome):
    G = nx.DiGraph()
    data = parse(file_name)
    for i in data:
        G.add_edge(i.split(' ')[0], i.split(' ')[1],weight = int(data[i][0]))
    return nx.shortest_path_length(G, start_genome, end_genome, weight = 'weight')





