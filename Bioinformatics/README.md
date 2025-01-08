### Build-Evolution-Tree
Examines DNA sequences of numerous bacteria/taxons and uses them to determine evolutionary relationship among the bacteria/taxons and construct a tree to represent this relationship. Then, tests the integrity of this tree through bootstrapping, whereby fake sequences are created based on random nucleotides taken from the bacteria/taxons used to create an original tree, and then these sequences are used to create their own trees which are then compared to the original tree to examine the original tree's validity.

### Codon-Analysis
This program reads in a DNA sequence and determines the proteins the sequence creates. Analysis is then conducted on the results.

### Disordered-Region Analysis
This program examines an aligned set of DNA sequences (So that the same parts of different DNA sequences are directly above/below one another), and determines how much each part of sequences differs from the others. Visualization and further analysis is then performed to make sense of these results.

### Needleman-Wunsch
Takes two DNA sequences as input, and aligns them so that each nucleotide in a DNA sequence corresponds with a part in the other nucleotide sequence and vice versa. Analysis is then conducted on the alignment. 

### Final-Project
Implements an algorithm entirely invented by myself to calculate the biodiversity of a biological sample. The calculation involves building a tree based on the sample and weighting each edge of the tree, such that adding up all edges with their given weight yields a calculation of diversity. The edges are weighted based on how skewed the subtrees connected by the edges are in relation to one another.