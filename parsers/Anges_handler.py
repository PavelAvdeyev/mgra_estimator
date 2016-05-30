import os

from parsers import Handler
import shutil
import graphs.BPG_from_grimm as BPGscript
import measures.Measures as Measures


class Anges_handler(Handler.Handler):
    def __init__(self):
        super(Anges_handler, self).__init__("Anges")
        #self.name_tool = "Anges"

    def parse_cars(self, dir_path):
        path_dir = os.path.join(dir_path, 'Anges', "TEL_BAB", 'CARS', 'NON_DUP_YEAST_PQRTREE_DOUBLED')
        genome = Handler.parse_genome_in_procars_file(path_dir)
        return genome

    '''
    Blocks file in Cars format, needs weightened trees, all combined in PARAMETERS file.
    '''
    def save(self, dir_path):
        anges_dir = os.path.join(dir_path, self.name_tool)

        if not os.path.exists(anges_dir):
            os.makedirs(anges_dir)

        blocks_txt = os.path.join(anges_dir, self.input_blocks_file)
        anges_tree_with_tag = os.path.join(anges_dir, "tree_tag.txt")
        anges_tree_txt = os.path.join(anges_dir, "tree.txt")
        tree_file_with_tag = os.path.join(dir_path, "tree.txt")
        tree_file_without_tag = os.path.join(dir_path, "bad_tree.txt")
        shutil.copy(tree_file_without_tag, anges_tree_txt)

        genomes = Handler.parse_genomes_in_grimm_file(os.path.join(dir_path, self.input_blocks_file))
        Handler.write_genomes_with_cars_in_file(blocks_txt, genomes)

        param_file = os.path.join(anges_dir, 'PARAMETERS.txt')

        with open(param_file, 'w') as f:
            n1 = '/n'
            lines = ['markers_file ' + blocks_txt + '/n', n1, 'tree_file ' + anges_tree_txt + '/n', n1,
                     'output_directory ' + anges_dir + '/results/n', n1, 'output_ancestor ANCESTOR/n',
                     n1, 'markers_doubled 0/n', n1, 'markers_unique 1/n', n1, 'markers_universal 2/n', n1,
                     '#acs_pairs PAIRS  [ACS_SPECIES_PAIRS_FILE_NAME] # name of file containing the species pairs to compare/n',
                     n1, 'acs_sa 1/n', n1, 'acs_ra 0/n', n1, 'acs_sci 0/n', n1, 'acs_mci 0/n', n1, 'acs_aci 0/n',
                     n1, '#acs_file ACS   [ACS_FILE_NAME] # ACS provided by user/n', n1, 'acs_weight 1/n',
                     n1, 'c1p_linear 1   # 0 for working with circular chromosomes/n', n1,
                     'c1p_circular 0 # 1 for working with a unique circular chromosomes/n', n1,
                     'c1p_telomeres 2 # 0: no telomere, 1: added after optimization (greedy heuristic), '
                    '2: added after optimization (bab), 3: added during optimization (bab)/n', n1,
                     'c1p_heuristic 0 # Using a greedy heuristic/n', n1, 'c1p_bab 0 # Using a branch-and-bound/n', n1,
                     'c1p_spectral 0 # Using spectral seriation/n', n1,
                     'c1p_spectral_alpha 1.0 # Spectral seriation alpha value']
            f.writelines(lines)
            # f.write('markers_file ' + blocks_txt + '/n')
            # f.write('tree_file ' + anges_tree_txt + '/n')
            # f.write('output_directory' + anges_dir + '/results/n')
            # f.write('output_ancestor ANCESTOR/n')
            # f.write('markers_doubled 0/n')
            # f.write('markers_unique 1/n')
            # f.write('markers_universal 2/n')
            # f.write('#acs_pairs PAIRS  [ACS_SPECIES_PAIRS_FILE_NAME] # name of file containing the species pairs to compare/n')
            # f.write('acs_sa 1/n')
            # f.write('acs_ra 0/n')
            # f.write('acs_sci 0/n')
            # f.write('acs_mci 0/n')
            # f.write('acs_aci 0/n')
            # f.write('#acs_file ACS   [ACS_FILE_NAME] # ACS provided by user/n')
            # f.write('acs_weight 1/n')
            # f.write('#acs_correction [0/1/2]    # Correcting for missing markers: 0 = none, 1 = adding markers spanned by intervals, 2 = X/n')
            # f.write('c1p_linear 1   # 0 for working with circular chromosomes/n')
            # f.write('c1p_circular 0 # 1 for working with a unique circular chromosomes/n')
            # f.write('c1p_telomeres 2 # 0: no telomere, 1: added after optimization (greedy heuristic), '
            #         '2: added after optimization (bab), 3: added during optimization (bab)/n')
            # f.write('c1p_heuristic 0 # Using a greedy heuristic/n')
            # f.write('c1p_bab 0 # Using a branch-and-bound/n')
            # f.write('c1p_spectral 0 # Using spectral seriation/n')
            # f.write('c1p_spectral_alpha 1.0 # Spectral seriation alpha value')




