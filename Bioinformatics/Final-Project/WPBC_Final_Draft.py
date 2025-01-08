import sys

# Dynamic Grouping Algorithm
# WPBC stands for weighted phylogenetic biodiversity calculator
# sample is expected to be a dictionary of species names as keys and abundance in sample as values. 
# tree_info is the edges.txt file as a double list.
def get_WPB(sample, tree_info):
    root_node = tree_info[len(tree_info)-1][0]

    n_species = len(sample.keys())
    n_nodes = len(tree_info)
    biodiversity = 0
    encountered = [] # To track which species have documented by the algorithm and are therefore already included in tracking the sample's phylogenetic span.

    info_indices = {}
    for i in range(n_nodes):
        info_indices[tree_info[i][1]] = i

    # Calculates the abundance of species underneath each node.
    descendants_abundance = {}
    for data in tree_info:
        child = data[1]
        parent = data[0]
        if child in sample.keys():
            descendants_abundance[child] = sample[child]
        
        if parent not in descendants_abundance.keys():
            descendants_abundance[parent] = 0

        # Adding 0.0001 so thst parents are treated as more abundant than their equally abundant children.
        # Purpose is so that parents are examined before children for their abundant off-spring
        descendants_abundance[parent] += descendants_abundance[child] + 0.0001

    # Calculates the descendant with the most abundance.
    max_children = {}
    for data in tree_info:
        child = data[1]
        parent = data[0]
        if child in sample.keys():
            max_children[child] = child
        
        if parent not in max_children.keys():
            max_children[parent] = max_children[child]
        
        if sample[max_children[parent]] < sample[max_children[child]]:
            max_children[parent] = max_children[child]

    # Orders the species based on which most strongly cause the largest groups to be large, so that large groups have tree constructions first
    species_by_abundance = []
    groups_by_abundance = sorted(descendants_abundance.keys(), key=lambda x: descendants_abundance[x], reverse=True)
    invalid_starting_node = [] 
    for group in groups_by_abundance:
        if group in invalid_starting_node:
            continue
        invalid_starting_node.append(group)
        children, descendants = get_partitioning(tree_info, group)
        most_abundant_child = group
        while(len(children) != 0):
            # Grabs the node's most abundant child 
            most_abundant_child = max(children, key=lambda x: descendants_abundance[x])
            invalid_starting_node.append(most_abundant_child) # The source of these nodes' high abundance will have already been captured on new iterations.
            children, descendants = get_partitioning(tree_info, most_abundant_child)
        species_by_abundance.append(most_abundant_child)

    # Holds the weight given to each edge.
    edge_weights = {}
    edge_weights[species_by_abundance[0]] = 1 # Arbitrary start value. 

    # Omits first element, since one node does not span a tree. 
    # We are treating the first element as having already been documented by the algorithm.
    encountered.append(species_by_abundance[0])
    species_by_abundance = species_by_abundance[1:n_species]


    for i, species in enumerate(species_by_abundance):
        # If the next species is not in the sample, the algorithm has gone through all specieis in the sample, and so it is finished.
        if sample[species] == 0:
            break
        
        weight = sample[species]
        new_nodes = []

        tree_contribution = 0.0
        current_node = species
        while(True):
            new_nodes.append(current_node)
            parent = tree_info[info_indices[current_node]][0]
            other_child, descendants = get_partitioning(tree_info, parent, current_node)


            # Checks for each encountered species whether it's the current node's parent's descendents.
            encountered_species_are_in_descendants = [encountered_species in descendants[0] for encountered_species in encountered]

            # If a root is encountered, there must be two sets of descendants and all species must be its descendants. 
            if len(descendants) == 2 or all(encountered_species_are_in_descendants):
                tree_contribution += float(tree_info[info_indices[current_node]][2])
                if len(descendants) == 2:
                    encountered_species_are_in_other_descendants = [encountered_species in descendants[1] for encountered_species in encountered]
                    if (all(encountered_species_are_in_descendants)):
                        child = other_child[0]
                    elif (all(encountered_species_are_in_other_descendants)):
                        child = other_child[1]
                    else:
                        # print(encountered)
                        # print(descendants)
                        # Takes the proportion of the new group of nodes' abundance to the rest of the tree's.
                        weight = descendants_abundance[current_node] / min(descendants_abundance[other_child[0]], descendants_abundance[other_child[1]])
                        weight *= edge_weights[parent]
                        break
                else:
                    child = other_child[0]
                new_nodes.append(parent)
                ancestor_child = child
                while(True):
                    new_nodes.append(child)
                    tree_contribution += float(tree_info[info_indices[child]][2])
                    children, descendants = get_partitioning(tree_info, child) 
                    if len(children) != 0:
                        encountered_species_come_from_first_child = [encountered_species in descendants[0] for encountered_species in encountered]
                        encountered_species_come_from_second_child = [encountered_species in descendants[1] for encountered_species in encountered]
                    if (len(children) != 0 and all(encountered_species_come_from_first_child)):
                        child = children[0]
                    elif (len(children) != 0 and all(encountered_species_come_from_second_child)):
                        child = children[1]
                    else:
                        # Takes the proportion of abundance of the new subtree being connected to the main tree, to the abundance of the main subtree.
                        # Each subtree from the decision point (The node in which both children were apart of the new subtree) is treated as a group here.
                        weight = descendants_abundance[current_node] / descendants_abundance[ancestor_child]
                        # Applies this proportion to the weight of its sister branch.
                        weight *= edge_weights[child]
                        break
                break

            elif any(encountered_species_are_in_descendants):
                tree_contribution += float(tree_info[info_indices[current_node]][2])

                # Takes the proportion of abundance of the new subtree being connected to the main tree, to the abundance of the main subtree.
                # Practically speaking, the new branch are weighted based on how significant they are compared to their sister branch.
                weight = descendants_abundance[current_node] / descendants_abundance[other_child[0]]

                # Applies this proportion to the weight of its sister branch.
                weight *= edge_weights[other_child[0]]
                break
            else:
                tree_contribution += float(tree_info[info_indices[current_node]][2])
                current_node = parent

        for node in new_nodes:
            edge_weights[node] = weight
        
        encountered.append(species)
        tree_contribution *= weight
        biodiversity += tree_contribution

        #print("Iteration", i)
        #print(edge_weights)

    return biodiversity
            



def get_partitioning(info, node, ignore_node="None"):
    children = []
    partition = []

    for row in info:
        parent_node = row[0]
        child_node = row[1]
        if parent_node == node and child_node != ignore_node:
            # Need to convert the returned set to tuple so that it can be added to the set.
            partition.append(tuple(get_descendent_tips(info, child_node)))
            children.append(child_node)
    return children, partition
    
            

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
    
edges_file_name = sys.argv[2]
edges_file_handler = open(edges_file_name, 'r')
edges_info = []

for edge in edges_file_handler:
    edge_info = edge.rstrip().split('\t')
    edges_info.append(edge_info)
edges_file_handler.close()

samples_file_name = sys.argv[1]
samples_file_handler = open(samples_file_name, 'r')

species_names = samples_file_handler.readline().rstrip().split('\t')
species_biodiversities = []

for sample in samples_file_handler:
    abundances = sample.rstrip().split('\t')
    species_abundances = {}
    for index, species_abundance in enumerate(abundances):
        species_abundances[species_names[index]] = float(species_abundance)
    biodiversity = get_WPB(species_abundances, edges_info)
    species_biodiversities.append(biodiversity)

samples_file_handler.close()

print(species_biodiversities)
print(sorted(list(range(2,len(species_biodiversities)+2)), key=lambda x: species_biodiversities[x-2]))




