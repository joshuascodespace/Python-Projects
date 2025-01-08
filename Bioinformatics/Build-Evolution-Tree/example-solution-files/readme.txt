# Example input and outputs

# Your program should be run like this (if using python):
python <programname> example.fna

# Your program should output these files:
genetic-distances.txt
edges.txt
bootstrap.txt

# Plots were generated with provided script:
Rscript ../plot-edges.r edges.txt example-tip-labels.txt tree.pdf
Rscript ../plot-edges.r edges.txt example-tip-labels.txt bootstrap.txt tree-bootstrap.pdf
