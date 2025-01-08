I am not responsible for creating the plot-edges.r code. All other code, however, I am responsible for. 

Run in the following order:
- `neighbor_joining.py`
- `create_bootstrap_samples.py`
- `bootstrap_testing.py`

OR

- `neighbor_joining.py`
- `installation_file.r`
- `plot-edges.r`

## `neighbor_joining.py`
This program takes a file of multiple aligned sequences as input, and outputs both a `genetic-distances.txt` and `edges.txt` file.

### `genetic-distances.txt`
Contains a quantification of how different one sequence is from another.

### `edges.txt`
The second containing three columns representing the edges of a phylogenetic tree created from the multiple aligned sequences input. Each edge represents a child/parent relationship on the tree. The first column is the bacteria/taxon/species that is the parent, and the second column is the child. The third column represents the length of the tree; that is, how much biological time has passed since the child evolved from the parent.

## `create_bootstrap_samples.py`
This program creates fake sequences based on random nucleotides taken from the bacteria/taxons used to create an original tree, and then these sequences are used to create their own trees

### bootstrapped_trees
Edge files similar to the above `edges.txt` creates from the fake sequnces created from the above `create_bootstrap_samples.py` file. 

### bootstrap_folder
Edge files similar to the above `edges.txt` creates from the fake sequnces created from the above `create_bootstrap_samples.py` file. This was used to test the efficacy of the `create_bootstrap_samples.py` program.

## `bootstrap_testing.py`
Compares bootstrapped trees created by the `create_bootstrap_samples.py` program to the original tree from `neighbor_joining.py` to examine the original tree's validity.

### `bootstrap.txt`
Reports how much each node in the original tree is consistent across the bootstrapped trees.

## `installation_file.r`
Installs r packages necessary to run `plot-edges.r`

## `plot-edges.r`
Creates a visualization of a tree based on `edges.txt` file.

### `tip-labels.txt`
List names for each taxon/bacteria on the tree that can be included in the visualization.

### `tree.pdf`
Output from `plot-edges.r` file.

### `tree-bootstrap.pdf`
Ouput from `plot-edges.r` that records the amount each node (taxon/bacteria) is supported by the above bootstrap testing within the visualization.

## example
Data that can be input into program to produce files in the folder "example-solution-files" as output. This is used for testing.

## example-solution-files
Contains output expected from running programs with example data.

## Input Files

### `example.fna`
Taxons DNA sequences that are multiple aligned; input to `neighbor_joining.py`

### `bacteria.fna`
Bacteria DNA sequences that are multiple aligned; input to `neighbor_joining.py`

### __pycache__
Included to aid visualization code.