## `Calculate-Order.py`
This program examines an aligned set of DNA sequences (So that the same parts of different DNA sequences are directly above/below one another), and determines how much each part of sequences differs from the others. 

### `seqs-with-primers.fna`
Input to `Calculate-Order.py` that contains an aligned set of DNA sequences.

### `Calculate-Order-Output.txt`
Output to `Calculate-Order.py` when `seqs-with-primers.fna` is input.

## `Find-And-Plot-Disorder.py`
Plots disorder calculated from `Calculate-Order.py` as a line graph. Then, calculates regions of the sequence that are overall ordered and disordered. Finally, plots both the disorder and the altogether disordered regions together.

### `Disorder-Plot.pdf`
Line graph output from `Find-And-Plot-Disorder.py` of disorder.

### `Disordered_Regions.txt`
Output from `Find-And-Plot-Disorder.py` stating which regions are disordered.

### `Disordered_regions-plot.pdf`
Line graph output from `Find-And-Plot-Disorder.py` of disorder, along with entire regions that are overall disordered.

### batchX
- batch1 creates phylogenetic trees based on largest disordered region
- batch2 creates phylogenetic trees based on shortest disordered region
- batch3 creates phylogenetic trees based on all regions

### `batchX_tree_page-0001.jpg`
Tree created from each batch as jpg

### `batchX_tree.pdf`
Tree created from each batch as pdf

### `batchX.fna`
Input used to create each trees