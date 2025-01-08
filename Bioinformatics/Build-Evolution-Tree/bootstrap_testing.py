import sys
# from trees_in_python_standalone import TreeNode

# Used ChatGPT to figure out how to read all text files from a folder.
import os

def get_partitioning(info, node):
    partition = set()

    for row in info:
        parent_node = row[0]
        if parent_node == node:
            # Need to convert the returned set to tuple so that it can be added to the set.
            partition.add(tuple(get_descendent_tips(info, row[1])))
    return partition
    
            

def get_descendent_tips(info, node):
    tips = set()
    node_is_parent = False
    for line in info:
        if line[0] == node:
            node_is_parent = True
            node_child = line[1]
            # To find the descendents of a node, we must find the descendents of its descendents.
            descendent_info = get_descendent_tips(info, node_child)

            # Adds the child's set of descendents to the parent's set.
            tips = tips.union(descendent_info)
    
    if node_is_parent:
        return tips
    else:
        tips.add(node)
        return tips

def get_all_partitions(info):
    partitions = {}
    nodes_traversed = []
    for edge in info:
    # Only need to partition each parent node once.
        if edge[0] in nodes_traversed:
            continue
        else:
            parent_node = edge[0]
            # tree_node = main_root_node
            nodes_traversed.append(parent_node)
            partition = get_partitioning(info, parent_node)
            partitions[parent_node] = partition 

    return partitions



main_file_name = sys.argv[1]
folder_path = "./" + sys.argv[2] + "/"
bstrapped_files = [file for file in os.listdir(folder_path)]
main_file_handler = open(main_file_name, "r")
nodes_traversed = []
main_file_content = []
n = len(bstrapped_files)


for line in main_file_handler:
    data = line.rstrip().split("\t")
    main_file_content.append([data[0], data[1], data[2]])

main_partitions = get_all_partitions(main_file_content)

bootstrap_partitions = []

for file_name in bstrapped_files:
    bootstrap_file_handler = open(folder_path + file_name, "r")

    bootstrap_file_content = []
    for line in bootstrap_file_handler:
        data = line.rstrip().split("\t")
        bootstrap_file_content.append([data[0], data[1], data[2]])
    partitions = get_all_partitions(bootstrap_file_content)
    bootstrap_partitions.append(list(partitions.values()))

output_file_name = "bootstrap.txt"
output_file_handler = open(output_file_name, "w")

for main_node in main_partitions.keys():
    main_partition = main_partitions[main_node]
    bootstrap_coverage_count = 0

    # Checks if partition of node exists anywhere in a given bootstrapped tree.
    # Regarding which, each partition of the bootstrapped tree is stored as an entry in a list
    for bootstrap_partition in bootstrap_partitions:
        if main_partition in bootstrap_partition:
            bootstrap_coverage_count += 1
    bootstrap_coverage_average = bootstrap_coverage_count / n

    print(main_node, bootstrap_coverage_average, sep='\t', file=output_file_handler)
    

