import sys

#Reads in input and output file; opens input file to read.
file_to_read = sys.argv[1]
output_file_name = sys.argv[2]

gene_file = open(file_to_read, "r")
# Puts each section of the file into a list. This allows us to remove the sections with metadata and no raw sequencing data.
gene_file_contents = gene_file.read().split()

# If a file section does not start with ATG or ATT, it is likely sequencing of no interest to us (metatdata)
# If it does, we add it into a final gene list that contains all information we want to work with
gene_contents_list = []
for word in gene_file_contents:
    if word[0:3] == "ATG" or word[0:3] == "ATT":
        gene_contents_list.append(word)



codon_counts = {}

# Counts up all codons and counts each observation in a dictionary, in which the key is the codon
# Using integer division so that any codons at the end not in a group of three don't get counted
for gene_contents in gene_contents_list:
    k = 0
    for index in range(len(gene_contents)//3):
        codon = gene_contents[index*3:(index+1)*3]
        if codon in codon_counts:
            codon_counts[codon] += 1
        else:
            codon_counts[codon] = 1
        # k, along with this if-statement, is added purely for problem 7, hint 2.
        if (codon == "TAA" or codon == "TGA" or codon == "TAG") and k < 10:
            k += 1
            print(3*index)
        

output_file = open(output_file_name, "w")

# Used chatGPT to get the dictionary to output so that the values are in sorted order.
for codon, count in sorted(codon_counts.items(), key=lambda item: item[1], reverse=True):
    output_file.write(codon + "," + str(count) + "\n")
    print(codon + "," + str(count))
