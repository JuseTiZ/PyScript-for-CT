import os
import argparse
from ete3 import Tree
from itertools import combinations
from scipy.stats import binom_test


parser = argparse.ArgumentParser(description = "calculate d statistic based on gene tree topology.")
parser.add_argument("-s", "--spetre", type = str, help = "Species tree.", required = True)
parser.add_argument("-g", "--gentre", type = str, help = "Dir of gene trees.", required = True)
parser.add_argument("-o", "--output", type = str, help = "Path and name of output file.", default = './abbababatest.csv')
args = parser.parse_args()


# 找出物种树中所有的四元组合
def find_quartets(species_tree):
    species = [leaf.name for leaf in species_tree.get_leaves()]
    # 使用到 itertools 的 combinations
    quartets = list(combinations(species, 4))
    return quartets

# 根据物种树拓扑结构给四元组合分配 P1...O
def assign_p1_p2_p3_o(quartet, species_tree):
    closest_pair = None
    min_distance = float('inf')
    # 寻找最近的物种对
    for pair in combinations(quartet, 2):
        distance = species_tree.get_distance(pair[0], pair[1])
        if distance < min_distance:
            closest_pair = pair
            min_distance = distance
    remaining_species = list(set(quartet) - set(closest_pair))
    # 寻找离最近物种对最近的物种赋予 P3，更远的赋予 o
    p3, o = sorted(remaining_species, key=lambda x: species_tree.get_distance(x, closest_pair[0]) + species_tree.get_distance(x, closest_pair[1]))
    return (*closest_pair, p3, o)


# 计算统计
def calculate_d_statistic(gene_trees_folder, quartet):
    p1, p2, p3, o = assign_p1_p2_p3_o(quartet, species_tree)
    abba_count = 0
    baba_count = 0
    total_trees = 0

    # 对基因树文件夹进行遍历
    abba_gene = ''
    baba_gene = ''

    for filename in os.listdir(gene_trees_folder):
        if filename.endswith(".treefile"):
            tree_path = os.path.join(gene_trees_folder, filename)
            gene_name = filename.split('.')[0] + ', '
            gene_tree = Tree(tree_path)
            # 判断基因树是否包含所有四元组物种
            if all(species in [leaf.name for leaf in gene_tree.get_leaves()] for species in quartet):
                total_trees += 1
                # 提取子树，判断子树是否属于 ABBA 或 BABA
                gene_tree.prune(quartet, preserve_branch_length=True)
                if gene_tree.check_monophyly([p1, p2], target_attr="name")[0] and gene_tree.check_monophyly([p3, o], target_attr="name")[0]:
                    continue
                elif gene_tree.check_monophyly([p1, p3], target_attr="name")[0] and gene_tree.check_monophyly([p2, o], target_attr="name")[0]:
                    baba_count += 1
                    baba_gene += gene_name
                elif gene_tree.check_monophyly([p1, o], target_attr="name")[0] and gene_tree.check_monophyly([p2, p3], target_attr="name")[0]:
                    abba_count += 1
                    abba_gene += gene_name

    # 计算 d 统计量和二项检验 P 值
    try:
        d_statistic = (abba_count - baba_count) / (abba_count + baba_count)
    except:
        d_statistic = 0
    p_value = binom_test(min(abba_count, baba_count), abba_count + baba_count, 0.5)
    baba_gene = baba_gene.strip(', ')
    abba_gene = abba_gene.strip(', ')

    return [p1, p2, p3, o, abba_count, baba_count, d_statistic, p_value, total_trees, abba_gene, baba_gene]


#运行部分
species_tree_file = os.path.abspath(args.spetre)
gene_trees_folder = os.path.abspath(args.gentre)
output_file = os.path.abspath(args.output)

species_tree = Tree(species_tree_file)
quartets = find_quartets(species_tree)
total_num = len(quartets)
compu_num = 0

with open(output_file, 'w') as o:
    o.write('p1\tp2\tp3\to\tabba_count\tbaba_count\td_statistic\tp_value\ttotal_trees\tabba_gene\tbaba_gene\n')
    result = []
    string_list = []
    for quartet in quartets:
        result[:] = calculate_d_statistic(gene_trees_folder, quartet)
        if result[4] == 0 and result[5] == 0 :
            compu_num += 1
            print(f'The progress is {compu_num}/{total_num}')
            if compu_num % 20 == 0:
                o.flush()
            continue
        string_list[:] = [str(element) for element in result]
        string = '\t'.join(string_list)
        o.write(string + '\n')
        compu_num += 1
        if compu_num % 20 == 0:
            o.flush()
        print(f'The progress is {compu_num}/{total_num}')
