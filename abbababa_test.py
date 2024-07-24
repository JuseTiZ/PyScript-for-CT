import os
import argparse
from ete3 import Tree
from itertools import combinations
from scipy.stats import binom_test

def find_quartets(species_tree):
    """Find all quartets in the species tree."""
    species = [leaf.name for leaf in species_tree.get_leaves()]
    return list(combinations(species, 4))

def assign_p1_p2_p3_o(quartet, species_tree):
    """Assign P1, P2, P3, and O based on species tree topology."""
    closest_pair, min_distance = None, float('inf')
    for pair in combinations(quartet, 2):
        distance = species_tree.get_distance(pair[0], pair[1])
        if distance < min_distance:
            closest_pair, min_distance = pair, distance
    remaining_species = list(set(quartet) - set(closest_pair))
    p3, o = sorted(remaining_species, key=lambda x: species_tree.get_distance(x, closest_pair[0]) + species_tree.get_distance(x, closest_pair[1]))
    return (*closest_pair, p3, o)

def calculate_d_statistic(gene_trees_folder, quartet, species_tree):
    """Calculate D statistic for a given quartet."""
    p1, p2, p3, o = assign_p1_p2_p3_o(quartet, species_tree)
    abba_count, baba_count, total_trees = 0, 0, 0
    abba_genes, baba_genes = [], []

    for filename in os.listdir(gene_trees_folder):
        if filename.endswith(".treefile"):
            tree_path = os.path.join(gene_trees_folder, filename)
            gene_tree = Tree(tree_path)
            if all(species in [leaf.name for leaf in gene_tree.get_leaves()] for species in quartet):
                total_trees += 1
                gene_tree.prune(quartet, preserve_branch_length=True)
                if gene_tree.check_monophyly([p1, p3], target_attr="name")[0] and gene_tree.check_monophyly([p2, o], target_attr="name")[0]:
                    baba_count += 1
                    baba_genes.append(filename.split('.')[0])
                elif gene_tree.check_monophyly([p1, o], target_attr="name")[0] and gene_tree.check_monophyly([p2, p3], target_attr="name")[0]:
                    abba_count += 1
                    abba_genes.append(filename.split('.')[0])

    d_statistic = (abba_count - baba_count) / (abba_count + baba_count) if (abba_count + baba_count) != 0 else 0
    p_value = binom_test(min(abba_count, baba_count), abba_count + baba_count, 0.5)
    
    return [p1, p2, p3, o, abba_count, baba_count, d_statistic, p_value, total_trees, ', '.join(abba_genes), ', '.join(baba_genes)]

def main():
    parser = argparse.ArgumentParser(description="Calculate D statistic based on gene tree topology.")
    parser.add_argument("-s", "--spetre", type=str, required=True, help="Species tree.")
    parser.add_argument("-g", "--gentre", type=str, required=True, help="Directory of gene trees.")
    parser.add_argument("-o", "--output", type=str, default='./abbababatest.csv', help="Path and name of output file.")
    args = parser.parse_args()

    species_tree = Tree(os.path.abspath(args.spetre))
    gene_trees_folder = os.path.abspath(args.gentre)
    output_file = os.path.abspath(args.output)
    
    quartets = find_quartets(species_tree)
    total_num = len(quartets)

    with open(output_file, 'w') as o:
        o.write('p1\tp2\tp3\to\tabba_count\tbaba_count\td_statistic\tp_value\ttotal_trees\tabba_genes\tbaba_genes\n')
        for idx, quartet in enumerate(quartets, 1):
            result = calculate_d_statistic(gene_trees_folder, quartet, species_tree)
            if result[4] == 0 and result[5] == 0:
                continue
            o.write('\t'.join(map(str, result)) + '\n')
            if idx % 20 == 0:
                o.flush()
            print(f'The progress is {idx}/{total_num}', end='\r')
    print('\nDone.')


if __name__ == "__main__":
    main()