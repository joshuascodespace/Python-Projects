# This program is written to create a bar plot for both codon and amino acid data, provided that a file with corresponding data is given.
# Please note that the "count_aminos.py" program creates a csv of amino acid counts from given files of codon counts.

import sys
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns

# Opens files input by the user, then puts each codon along with its respective count into a list.
first_input_file_name = sys.argv[1]
first_input_file = open(first_input_file_name, "r")
first_input_file_contents = first_input_file.read().splitlines()

second_input_file_name = sys.argv[2]
second_input_file = open(second_input_file_name, "r")
second_input_file_contents = second_input_file.read().splitlines()


# A double list to tore information for each file line. This is later turned into a DataFrame for visualization purposes.
information = []

# In each row of this information double list, is the codon, followed by its count (listed in file), followed by which file it's from.
for first_stat in first_input_file_contents:
    codon = first_stat[0:3]
    count = int(first_stat[4:len(first_stat)])
    information.append([codon, count, "Coding sequences (correct frame shift)"])

for second_stat in second_input_file_contents:
    codon = second_stat[0:3]
    count = int(second_stat[4:len(second_stat)])
    information.append([codon, count, "Whole genome (random frame shift)"])

# Allows for seaborn visualization of data.
my_data = pd.DataFrame(information, columns=["Codons", "Counts", "Legend"])
my_data["Counts"].astype('int')

width = 12
height = 5
plt.figure(figsize=(width, height))
barplot = sns.barplot(data=my_data, x="Codons", y="Counts", hue="Legend")

plt.xlabel("Codon")

# Rotates labels so that x-axis is visible.
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=90)
plt.ylabel("Frequency")

plt.show()
