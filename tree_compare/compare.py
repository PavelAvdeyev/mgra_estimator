__author__ = 'nikita_kartashov'

from sys import argv

import dendropy as dp

from unrooted_tree import UnrootedBinaryTree


taxa = dp.TaxonSet()


def nt(s):
    return dp.Tree.get_from_string(s, 'newick', taxon_set=taxa, as_unrooted=True)


def strip_argument(argument):
    return argument.strip("\"")


def main():
    if len(argv) < 3:
        print("Need to input 2 trees in newick format")
        exit(1)
    left_tree = nt(strip_argument(argv[1]))
    right_tree = nt(strip_argument(argv[2]))
    t1 = UnrootedBinaryTree(left_tree.nodes()[0])
    t2 = UnrootedBinaryTree(right_tree.nodes()[0])
    print('Left tree: {0}'.format(left_tree.as_newick_string()))
    print('Right tree: {0}'.format(right_tree.as_newick_string()))
    print(left_tree.symmetric_difference(right_tree))
    print('\n'.join(t1.pretty_branches(t1.compare_branches(t2))))
    print('Distance difference: {0}'.format(t1.compare_distances(t2)))


if __name__ == '__main__':
    main()

