from parsers import PMAG_PLUS_handler, Handler, GASTS_handler, GapAdj_handler, MGRA_handler, Procars_handler, infercarspro_handler, Rococo_handler, Anges_handler



ancestor = GASTS_handler.GASTS_handler().parse('/media/hamster/UUI/RealData/fungal_genomes/Fungi')['3']
ancestor2 = Procars_handler.Procars_handler().parse('/media/hamster/UUI/RealData/fungal_genomes/Fungi')
ancestor3 = MGRA_handler.MGRA_handler().parse('/media/hamster/UUI/RealData/fungal_genomes/Fungi')['3']
ancestor4 = Anges_handler.Anges_handler().parse_cars('/media/hamster/UUI/RealData/fungal_genomes/Fungi')

simul = set()
simul2 = set()
simul3 = set()
simul4 = set()

def create_adjacency_set(input_set, genome):
    get_left = lambda gene: gene
    get_right = lambda gene: -gene

    for chromosome in genome:
        chr = list(chromosome)
        if chromosome.is_circular():
            input_set.add((min(get_right(chr[-1]), get_left(chr[0])), max(get_right(chr[-1]), get_left(chr[0]))))
        elif not chromosome.is_circular():
            input_set.add((min(0, get_left(chr[0])), max(0, get_left(chr[0]))))
            input_set.add((min(get_right(chr[-1]), 0), max(get_right(chr[-1]), 0)))

        for prev, next in zip(chr, chr[1:]):
            input_set.add((min(get_right(prev), get_left(next)), max(get_right(prev), get_left(next))))


create_adjacency_set(simul, ancestor)
create_adjacency_set(simul2, ancestor2)
create_adjacency_set(simul3, ancestor3)
create_adjacency_set(simul4, ancestor4)
only_gasts = 0
only_pro = 0
only_mgra = 0
gasts_mgra = 0
gasts_pro = 0
mgra_pro = 0
common = 0

for i in simul:
    if i in simul2:
        if i in simul3:
            common += 1
        else:
            gasts_pro += 1
    elif i in simul3:
        gasts_mgra += 1
    else:
        only_gasts += 1

for i in simul2:
    if i not in simul:
        if i in simul3:
            mgra_pro += 1
        else:
            only_pro += 1

for i in simul3:
    if i not in simul and i not in simul2:
        only_mgra += 1

print(only_gasts, only_pro, only_mgra, gasts_pro, gasts_mgra, mgra_pro, common)