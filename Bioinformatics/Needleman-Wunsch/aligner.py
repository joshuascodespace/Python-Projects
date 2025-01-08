import argparse

# Global variables
codon_amino_conversion = {"AAA": "K", "AAC": "N", "AAG": "K", "AAT": "N", "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T", "AGA": "R", "AGC": "S", "AGG": "R", "AGT": "S", "ATA": "I", "ATC": "I", "ATG": "M", "ATT": "I", "CAA": "Q", "CAC": "H", "CAG": "Q", "CAT": "H", "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P", "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R", "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L", "GAA": "E", "GAC": "D", "GAG": "E", "GAT": "D", "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A", "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G", "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V", "TAA": "O", "TAC": "Y", "TAG": "O", "TAT": "Y", "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S", "TGA": "O", "TGC": "C", "TGG": "W", "TGT": "C", "TTA": "L", "TTC": "F", "TTG": "L", "TTT": "F"}

# Below copied from Homework 2 Instructions

# set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', required=True, type=str)
parser.add_argument('-r', '--reference', required=True, type=str)
parser.add_argument('-o', '--output', required=True, type=str)
parser.add_argument('-g', '--gap_penalty', required=True, type=int)
parser.add_argument('-p', '--mismatch_penalty', required=True, type=int)
parser.add_argument('-m', '--match_score', required=True, type=int)
parser.add_argument('--ignore_outer_gaps', action='store_true')

# parsing arguments to get variables (can rename variables as desired)
args = parser.parse_args()
query_file = args.query
ref_file = args.reference
output_file = args.output
gap_penalty = args.gap_penalty
mismatch = args.mismatch_penalty
match = args.match_score
ignore_start_end_gaps = args.ignore_outer_gaps


query_file_handler = open(query_file, "r")
ref_file_handler = open(ref_file, "r")

query_file_header = query_file_handler.readline().rstrip()
ref_file_header = ref_file_handler.readline().rstrip()
query = query_file_handler.readline().rstrip()
ref = ref_file_handler.readline().rstrip()
query_file_handler.close()
ref_file_handler.close()

# For question 7 and 8.
def translate_nucleotides_to_amino_acids(nucleotides, output_file_name):
    # Need to start translations only after an ATG codon is encountered.
    start_index = 0
    while(nucleotides[0+start_index:3+start_index] != "ATG"):
        start_index += 1
    
    #Constructs string of amino acid; starts counting at i = 3, since ATG is preemptively counted.
    amino_acids = codon_amino_conversion["ATG"]
    i=3
    #While loops checks whether stop codon was encounted at previous iteration, and adds on amino acids otherwise.
    while(not nucleotides[start_index+i-3:start_index+i] in {"TGA", "TAA", "TAG"}):
        amino_acids += codon_amino_conversion[nucleotides[start_index+i:start_index+i+3]]
        i += 3
    output_file_handler = open(output_file_name, "w")
    print(amino_acids, file=output_file_handler)
    output_file_handler.close()
    return amino_acids

# For question 7 and 8:
# query = translate_nucleotides_to_amino_acids(query, "pfizer_mrna.aa")
# ref = translate_nucleotides_to_amino_acids(ref, "sars_spike_protein.aa")


m = len(query)
n = len(ref)


    

previous_direction_matrix = [['l' for column in range(n)] for row in range(m)]
if ignore_start_end_gaps:
    # Initializes a matrix to zero to store scores of each alignment
    best_score_matrix = [[0 for column in range(n+1)] for row in range(m+1)]
else:
    # Initializes the matrix to score as if all gaps were the best score.
    # Forces start gap penalty. Algorithm will presumably rewrite all other data.
    best_score_matrix = [[gap_penalty*column + gap_penalty*row for column in range(n+1)] for row in range(m+1)]

for j in range(1, m+1):
    for i in range(1, n+1):
        # Classic Needleman-Wunsch
        
        from_above_score = best_score_matrix[j-1][i] + gap_penalty
        # print(i, j-1, len(best_score_matrix), len(best_score_matrix), n)
        from_left_score = best_score_matrix[j][i-1] + gap_penalty
        
        if query[j-1] == ref[i-1]:
            from_match_score = best_score_matrix[j-1][i-1] + match
        else:
            from_match_score = best_score_matrix[j-1][i-1] + mismatch
        # print(len(query), j-1, len(ref), i-1)
        # Finds the best direction to come from in the matrix, and records it in a different matrix.
        current_score = from_left_score
        if from_above_score > from_left_score:
            current_score = from_above_score
            previous_direction_matrix[j-1][i-1] = 'u'
            # print(i, j, n, m)
        if from_match_score > current_score:
            current_score = from_match_score
            previous_direction_matrix[j-1][i-1] = 'ul'

        best_score_matrix[j][i] = current_score

i = n
j = m
if ignore_start_end_gaps:
    max_rightmost_index = 0
    # Finds the best row in the last column
    for row in range(m+1):
        if best_score_matrix[row][n] > best_score_matrix[max_rightmost_index][n]:
            max_rightmost_index = row
    max_bottommost_index = 0
    # Finds the best column in the last row
    for col in range(n+1):
        if best_score_matrix[m][col] > best_score_matrix[n][max_bottommost_index]:
            max_bottommost_index = col
    
    # Compares the best row to the best column. Sets the best end alignment to be the index of i and j.
    if best_score_matrix[max_rightmost_index] > best_score_matrix[max_bottommost_index]:
        j = max_rightmost_index
    else:
        i = max_bottommost_index

final_score = best_score_matrix[j][i]

# Idea is to build reference genome from the start by adding gaps and emissions as they are determined to occur from algorithm. 
new_query = ""
new_reference = ""
# To keep track of which states are encountered during backtracking;.
match_type = ""

# These lines put in end gaps preemptively, so that the loop can start in the middle a query/reference sequence if needed.
for gap in range(m-j):
    new_reference += "_"
    new_query += query[m-gap-1]
    match_type += ' '
    
for gap in range(n-i):
    new_query += "_"
    new_reference = ref[n-gap-1]
    match_type += ' '

# For part 6 and 9.
mismatch_count = 0

while(i > 0 and j > 0):
    if previous_direction_matrix[j-1][i-1] == 'l':
        i -= 1
        new_query += "_"
        new_reference += ref[i]
        match_type += ' '
        mismatch_count += 1
    elif previous_direction_matrix[j-1][i-1] == 'u':
        j -= 1
        new_reference += "_"
        new_query += query[j]
        match_type += ' '
        mismatch_count += 1
    else:
        i -= 1
        j -= 1
        new_query += query[j]
        new_reference += ref[i]
        # Need to know whether alignment was a match or mismatch
        if query[j] == ref[i]:
            match_type += '|'
        else:
            match_type += 'x'
            mismatch_count += 1

# Adds start gaps into aligned sequences. Cannot do in while loop, because no left/upper cell to check.
for gap in range(j):
    new_query += query[j-gap-1]
    new_reference += '_'
    match_type += ' '
for gap in range(i):
    new_reference += ref[i-gap-1]
    new_query += '_'
    match_type = ' '

# Print only for question 6 and 9:
print(mismatch_count)

def flip_string(to_flip, length):
    new_string = ""
    for i in range(length):
        new_string += to_flip[length-i-1]
    return new_string

# Strings are created starting from their ends; need to flip them.
new_query = flip_string(new_query, len(new_query))
new_reference = flip_string(new_reference, len(new_reference))
match_type = flip_string(match_type, len(match_type))




# Writing data out to file.
output_file_handler = open(output_file, "w")
print(final_score, file=output_file_handler)
print(ref_file_header, file=output_file_handler)
print(new_reference, file=output_file_handler)
print(match_type, file=output_file_handler)
print(new_query, file=output_file_handler)
print(query_file_header, file=output_file_handler)
output_file_handler.close()