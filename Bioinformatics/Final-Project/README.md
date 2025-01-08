# Lead up code/files to algorithm

## `neighbor_joining.py`
This program takes a file of multiple aligned sequences as input, and outputs both a `genetic-distances.txt` and `edges.txt` file.

### `genetic-distances.txt`
Contains a quantification of how different one sequence is from another.

### `edges.txt`
The second containing three columns representing the edges of a phylogenetic tree created from the multiple aligned sequences input. Each edge represents a child/parent relationship on the tree. The first column is the bacteria/taxon/species that is the parent, and the second column is the child. The third column represents the length of the tree; that is, how much biological time has passed since the child evolved from the parent.

## `samples.txt`
A file that represents an arbitrary set of proportions of species/taxons/bacteria from given biological samples.

## `plot-edges.r`
Creates a visualization of a tree based on `edges.txt` file.

### `tip-labels.txt`
List names for each taxon/bacteria on the tree that can be included in the visualization.

### `tree.pdf`
Output from `plot-edges.r` file.

## Input Files

### `example.fna`
Taxons DNA sequences that are multiple aligned; input to `neighbor_joining.py`

### `bacteria.fna`
Bacteria DNA sequences that are multiple aligned; input to `neighbor_joining.py`


# Algorithm Code

### `UPBC.py`
Unweighted phylogenetic biodiversity calculator. It finds the biodervisity of a sample by adding up all branches on a phylogenetic tree that connects species in a sample. 

### `WPBC_Initial_Draft.py`
Weighted phylogenetic biodiversity calculator. Used initial algorithm discussed in report below.

### `WPBC_Initial_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `UPBC.py`.
-  Use abundance of species as multiplier to edge weights connect species to the rest of the tree. Do from most yo least abundant species

### `WPBC_Second_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `WPBC_Initial_Draft.py`. 
- Use abundance of all descendants combined of any node as a multiplier to any given tree. 
-  A tree with two distantly related groups where each group has very few species of high abundance would fare more well with draft 1 than if each group had many species of relatively low abundance, which is backwards

### `WPBC_Third_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `WPBC_Second_Draft.py`. 
- Instead of going to most to least abundant species, go to most to least abundant group (group = collection of all a node’s descendants)
- A tree with two distantly related groups where one group has very few species of high abundance and the other has many species of relatively low abundance would have an extremely high multiplier throughout the tree, which gives this tree an unfair advantage.

### `WPBC_Fourth_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `WPBC_Third_Draft.py`. 
- Edges multiplied by the ratio of the species abundance to the descendant with the maximum abundance of a node’s descendants. This ratio is a group’s total abundance.
- Splitting up a group to have more species does not benefit any species, as branch lengths might be, for example, doubled, and branch weights would be halved, therefore evening out. This strategy is also still mindful of highly disproportionate groups, giving a species that dominates a group by far the most weight within that group.

### `WPBC_Fifth_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `WPBC_Fourth_Draft.py`. 
- Edges multiplied by ratio of the currently examined group to group being connected to. 
- This solves the issue of connected groups being sometime disproportionately unbalanced due to some edges getting weight far exceeding its species abundance due to recalculation of weight. This also has more theoretical backing, as the algorithm essentially has all branches at 1 with 100% uniform distribution, with penalties only applying to  unevenness.

### `WPBC_Sixth_Draft.py`
Weighted phylogenetic biodiversity calculator. Updated from `WPBC_Fifth_Draft.py`. 
- Pretends the branch adding the first species to the tree has a weight of 1.
- This is done to prevent penalties being applied twice to a branch. Connecting to the largest part of the tree means that the only disproportionality exists between the new branches connection with the original. Thus, it doesn't make sense to apply any further penalty to the branch.

### `WPBC_Final_Draft.py`
Weighted phylogenetic biodiversity calculator. Same as `WPBC_Sixth_Draft.py`. 





# Report

### `Final Project.pdf`
Formally reports the research conducted for this project, the process used to conduct the research, and analysis of discoveries from research.





