import sys

input_file = sys.argv[1]
input_file_handler = open(input_file, 'r')
output_file = "genetic-distances.txt"
output_file_handler = open(output_file, "w")
genetic_distances = []
genes = []

for line in input_file_handler:
    # Skip reading in header lines; only interested in gene sequences.
    if line.find(">") != -1:
        continue
    else:
        # Need to make sure to remove the trailing newline character.
        genes.append(line.rstrip())

input_file_handler.close()
n=len(genes[0]) 
gene_count = len(genes)

for gene_i_index, gene_i in enumerate(genes):
    # Each gene gets a row for distances between itself and all other genes.
    genetic_distances.append([])
    for gene_j_index, gene_j in enumerate(genes):
        dissimilarity_count = 0
        if gene_j_index > gene_i_index:
            for char_index in range(n):
                # Compares genes character by character checking for dissimilarity/inequality.
                if gene_i[char_index] != gene_j[char_index]:
                    dissimilarity_count+=1
            percent_dissimilarity = dissimilarity_count / n
            genetic_distances[gene_i_index].append(percent_dissimilarity)
        elif gene_i_index == gene_j_index:
            # All diagonal entries will be 0.0
            genetic_distances[gene_i_index].append(0.0)
        else:
            # All upper triangle entries will be equal to their transposed element
            genetic_distances[gene_i_index].append(genetic_distances[gene_j_index][gene_i_index])
        if gene_j_index < gene_count - 1:
            print(genetic_distances[gene_i_index][gene_j_index], end='\t', file=output_file_handler)
        else:
            print(genetic_distances[gene_i_index][gene_count-1], file=output_file_handler)
output_file_handler.close()
        
# To keep track of which ID each gene in the distance matrix corresponds to as it gets edited
node_IDs = list(range(1, gene_count + 1))

edges_file = 'edges.txt'
edges_file_handler = open(edges_file, "w")

while(gene_count >= 3):
    score_matrix = []
    
    # Populate score matrix
    min_score = [0,0]
    for i in range(gene_count):
        # Each gene gets a row for score between itself and all other genes.
        score_matrix.append([])
        for j in range(gene_count):
            if i < j:
                i_distance_sum = 0
                j_distance_sum = 0
                for k in range(gene_count):
                    # Adds up distances from two different genes to all other genes.
                    if k == i or k == j:
                        continue
                    else:
                        i_distance_sum += genetic_distances[i][k]
                        j_distance_sum += genetic_distances[j][k]
                # Formula for score; distance between two genes is unfavorable, distance to all other genes is favorable.
                # Commented out is code that doesn't count i's and j's distance in the sums from i and j to everything else. Seems more intuitively accurate, but had to change code to match the example2 data and wikipedia article.
                # score = (gene_count-2)*genetic_distances[i][j]-i_distance_sum-j_distance_sum
                score = (gene_count-4)*genetic_distances[i][j]-i_distance_sum-j_distance_sum
                # Checking for minimum score as scores are calculated. Records index of minimum score.
                if score < score_matrix[min_score[0]][min_score[1]]:
                    min_score = [i, j]
                score_matrix[i].append(score)
            elif i > j:
                # Score matrix is symmetric; avoids unnecessary double computation.
                score_matrix[i].append(score_matrix[j][i])
            else: 
                # gene_count-2 is the largest any entry; 
                # appending gene count to the diagonals ensures that they are not less than other entries.
                score_matrix[i].append(gene_count)
    i = min_score[0]
    j = min_score[1]
    distance_i_j =  genetic_distances[i][j]
    average_different_distance_i_j = 0
    for k in range(gene_count):
        # Calculates exactly how much further i is from all other genes compared to j as a sum of their distances.
        if i == k or j == k:
            continue
        else:
            average_different_distance_i_j += genetic_distances[i][k]
            average_different_distance_i_j -= genetic_distances[j][k]
    # Formulas for new distances from parent node to child nodes.
    i_to_new_distance = 1/2 * distance_i_j + 1/(2 * (gene_count - 2)) * average_different_distance_i_j
    j_to_new_distance = distance_i_j - i_to_new_distance
    new_node_distances = []
    for k in range(gene_count):
        # Calculated distances between parent node and all other nodes using neighbor joining formula.
        if k == i or k == j:
            # Need to make sure the list is the same size as distance matrix.
            new_node_distances.append(float("nan"))
            continue
        else:
            new_distance = 1/2 *(genetic_distances[k][i] + genetic_distances[k][j] - distance_i_j)
            new_node_distances.append(new_distance)
    # This is the node's distance from itself.
    new_node_distances.append(0.0)

    # Adds the new node's ID to the list of node IDs.
    node_IDs.append(node_IDs[len(node_IDs)-1] + 1)

    # Attach final node to the new parent too if only three nodes are left unplaced.
    if gene_count == 3:
        # With three elements, only 0, 1 and 2 are possible indices for i, j, and k. Thus, the kth index is whichever index is neither i nor j.
        if i != 0 and j != 0:
            k = 0
        elif i != 1 and j != 1:
            k = 1
        elif i != 2 and j != 2:
            k = 2
        else:
            # Done to detect potential errors
            k = float("nan")
        
        # Connects last node to most recently created parent to finish the tree.
        distance_i_k = genetic_distances[i][k]
        k_to_new_distance = distance_i_k - i_to_new_distance
        print(node_IDs[3], node_IDs[k], k_to_new_distance, file=edges_file_handler, sep='\t')
        gene_count -= 1

    # Adds edges formed coming out of the new node outwards in the format requested
    print(node_IDs[len(node_IDs)-1], node_IDs[i], i_to_new_distance, file=edges_file_handler, sep='\t')
    print(node_IDs[len(node_IDs)-1], node_IDs[j], j_to_new_distance, file=edges_file_handler, sep='\t')

    # Updates genetic distances to disclude all distances involving i and j, and add distances involving i and j's parent node at the matrix's end.
    if i < j:
        genetic_distances = [row[0:i] + row[i+1:j] + row[j+1:gene_count] + new_node_distances[x:x+1] for x, row in enumerate(genetic_distances) if x != i and x != j]
        # Update list dimensions to match updated matrix dimensions
        del new_node_distances[j]
        del new_node_distances[i]

        # Deletes old nodes from list. Done in if-statement, since deleting an earlier index changes later indexes.
        del node_IDs[j]
        del node_IDs[i]

    else:
        genetic_distances = [row[0:j] + row[j+1:i] + row[i+1:gene_count] + new_node_distances[x:x+1] for x, row in enumerate(genetic_distances) if x != i and x != j]
        # Update list dimensions to match updated matrix dimensions
        del new_node_distances[i]
        del new_node_distances[j]

        # Deletes old nodes from list. Done in if-statement, since deleting an earlier index changes later indexes.
        del node_IDs[i]
        del node_IDs[j]
    
    genetic_distances.append(new_node_distances)

    gene_count -= 1

