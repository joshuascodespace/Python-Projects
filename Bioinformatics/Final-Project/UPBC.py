import sys

# This is an unweighed phylogenetic biodiversity calculator.
# sample is expected to be a dictionary of species names as keys and abundance in sample as values. 
# tree_info is the edges.txt file as a double list.
def get_UPB(sample, tree_info):
    # Creates list of which species appear most to least
    species_by_abundance = sorted(sample.keys(), key=lambda x: sample[x], reverse=True)
    n_species = len(sample.keys())
    n_nodes = len(tree_info)
    biodiversity = 0
    encountered = [] # To track which species have documented by the algorithm and are therefore already included in tracking the sample's phylogenetic span.

    

    info_indices = {}
    for i in range(n_nodes):
        info_indices[tree_info[i][1]] = i

    # Calculates term to normalize diversity calculation for consistency across data.
    normalization_term = 0.0
    for row in tree_info:
        normalization_term += float(row[2])

    # Omits first element, since one node does not span a tree. 
    # We are treating the first element as having already been documented by the algorithm.
    encountered.append(species_by_abundance[0])
    species_by_abundance = species_by_abundance[1:n_species]

    for i, species in enumerate(species_by_abundance):
        # If the next species is not in the sample, the algorithm has gone through all specieis in the sample, and so it is finished.
        if sample[species] == 0:
            break
        
        weight = 1 # Change 1 to sample[species] to make niave weighted calculation algorithm
        tree_contribution = 0
        current_node = species
        while(True):
            parent = tree_info[info_indices[current_node]][0]
            children, descendants = get_partitioning(tree_info, parent, current_node)


            # Checks for each encountered species whether it's the current node's parent's descendents.
            encountered_species_are_in_descendants = [encountered_species in descendants[0] for encountered_species in encountered]

            # If a root is encountered, there must be two sets of descendants and all species must be its descendants. 
            if len(descendants) == 2 or all(encountered_species_are_in_descendants):
                tree_contribution += float(tree_info[info_indices[current_node]][2]) * weight
                if len(descendants) == 2:
                    encountered_species_are_in_other_descendants = [encountered_species in descendants[1] for encountered_species in encountered]
                    if (all(encountered_species_are_in_descendants)):
                        child = children[0]
                    elif (all(encountered_species_are_in_other_descendants)):
                        child = children[1]
                    else:
                        break
                else:
                    child = children[0]
                while(True):
                    tree_contribution += float(tree_info[info_indices[child]][2]) * weight
                    children, descendants = get_partitioning(tree_info, child)
                    if len(children) != 0:
                        encountered_species_come_from_first_child = [encountered_species in descendants[0] for encountered_species in encountered]
                        encountered_species_come_from_second_child = [encountered_species in descendants[1] for encountered_species in encountered]
                    if (len(children) != 0 and all(encountered_species_come_from_first_child)):
                        child = children[0]
                    elif (len(children) != 0 and all(encountered_species_come_from_second_child)):
                        child = children[1]
                    else:
                        break
                break

            elif any(encountered_species_are_in_descendants):
                tree_contribution += float(tree_info[info_indices[current_node]][2]) * weight
                break
            else:
                tree_contribution += float(tree_info[info_indices[current_node]][2]) * weight
                current_node = parent
        
        encountered.append(species)
        biodiversity += tree_contribution

    biodiversity /= normalization_term
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
    biodiversity = get_UPB(species_abundances, edges_info)
    species_biodiversities.append(biodiversity)

samples_file_handler.close()

print(species_biodiversities)
