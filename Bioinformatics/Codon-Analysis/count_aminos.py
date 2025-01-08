import sys

# Opens files input by the user, then puts each codon along with its respective count into a list.
file_to_read = sys.argv[1]
output_file_name = sys.argv[2]

codon_file = open(file_to_read, "r")
codon_file_contents = codon_file.read().splitlines()

# Dictionary maps each codon to any amino-acid.
codon_amino_conversion = {"AAA": "Lys", "AAC": "Asn", "AAG": "Lys", "AAT": "Asn", "ACA": "Thr", "ACC": "Thr", "ACG": "Thr", "ACT": "Thr", "AGA": "Arg", "AGC": "Ser", "AGG": "Arg", "AGT": "Ser", "ATA": "Ile", "ATC": "Ile", "ATG": "Met", "ATT": "Ile", "CAA": "Gln", "CAC": "His", "CAG": "Gln", "CAT": "His", "CCA": "Pro", "CCC": "Pro", "CCG": "Pro", "CCT": "Pro", "CGA": "Arg", "CGC": "Arg", "CGG": "Arg", "CGT": "Arg", "CTA": "Leu", "CTC": "Leu", "CTG": "Leu", "CTT": "Leu", "GAA": "Glu", "GAC": "Asp", "GAG": "Glu", "GAT": "Asp", "GCA": "Ala", "GCC": "Ala", "GCG": "Ala", "GCT": "Ala", "GGA": "Gly", "GGC": "Gly", "GGG": "Gly", "GGT": "Gly", "GTA": "Val", "GTC": "Val", "GTG": "Val", "GTT": "Val", "TAA": "Stp", "TAC": "Tyr", "TAG": "Stp", "TAT": "Tyr", "TCA": "Ser", "TCC": "Ser", "TCG": "Ser", "TCT": "Ser", "TGA": "Stp", "TGC": "Cys", "TGG": "Trp", "TGT": "Cys", "TTA": "Leu", "TTC": "Phe", "TTG": "Leu", "TTT": "Phe"}

# Creates a list of all occurances of amino acids based on codon counts.
amino_acids = []
for codon_info in codon_file_contents:
    codon = codon_info[0:3]
    count = int(codon_info[4:len(codon_info)])
    amino_acid = codon_amino_conversion[codon]
    # This intentionally produces duplicate values with the intention of communicating plurality of amino acid existence to later code.
    for index in range(count):
        amino_acids.append(amino_acid)


output_file = open(output_file_name, "w")

amino_counts = {}

# Counts up each occurrance of amino acids documents, and puts them into a libary, in which the key is the amino acid, and the value is the count.
for amino_acid in amino_acids:
    if amino_acid in amino_counts:
        amino_counts[amino_acid] += 1
    else:
        amino_counts[amino_acid] = 1


# Used chatGPT to get the dictionary to output so that the values are in sorted order.
for amino_acid, count in sorted(amino_counts.items(), key=lambda item: item[1], reverse=True):
    output_file.write(amino_acid + "," + str(count) + "\n")
    print(amino_acid + "," + str(count))

