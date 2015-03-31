import os
import sys

from parsers import MGRA_handler, GapAdj_handler, GASTS_handler, PMAG_PLUS_handler

LIB_DIR = "lib"
ragout_root = os.path.dirname(os.path.realpath(__file__))
lib_absolute = os.path.join(ragout_root, LIB_DIR)
sys.path.extend([ragout_root, lib_absolute])
os.environ["PATH"] += os.pathsep + lib_absolute


tools = [
    MGRA_handler.MGRA_handler(),
    PMAG_PLUS_handler.PMAG_PLUS_handler(),
    GapAdj_handler.GapAdj_handler(),
    GASTS_handler.GASTS_handler()
]

def filter_genomes_by_species(target, params):
    species, genome, rear, indel_ratio = params
    if species == target:
        return True
    else:
        return False

