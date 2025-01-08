import numpy as np
import matplotlib.pyplot as plt

input_file_name = "solution-problem-1.txt"
input_file_handler = open(input_file_name, "r")

# Value determined by changing "bin_size" to many different values, Less than 25 had too much noise and variability. More than 25 had too few features.

bin_size = 25
histogram = []

for count, frequency in enumerate(input_file_handler):
    frequency = float(frequency.rstrip())

    # Creates a new bin every time bin_size worth of values are encountered.
    if count % bin_size == 0:
        histogram.append(0)
    # Adds the next frequency to the the ith bin, normalizing by the bin length each time.
    histogram[count // bin_size] += frequency / bin_size

if count % bin_size != 0:
    del histogram[len(histogram)-1]

input_file_handler.close()

xlist = np.linspace(0, bin_size * len(histogram) - bin_size, num=len(histogram))

plt.figure(num=0, dpi=120)
plt.plot(xlist, histogram, label="Sliding window average")
plt.xlabel("Base Pairs")
plt.ylabel("%Sequence Identity")

plt.savefig("solution-problem-2.pdf", format='pdf')

plt.show()




# PROBLEM 3 STARTS HERE:

graph_percentage_shown_for_variable_region = 85

variable_region_starts = []
variable_regions_ends = []

output_file_name = "solution-problem-3.txt"
output_file_handler = open(output_file_name, "w")

in_variable_region = False

# Upon viewing the figure from problem 2, it appears that there are about 9 regions that sink significantly low.
# More preciesly, it seems somewhat irregular and significant for the frequency to sink below 60, so that was dubbed the disordered region.
# Alternatively, this code can be ran such that an ordered region is somewhat irregular and significant
# In which case 80 is a good threshold, and about 10 regions go that high
for base_pair_group, frequency in enumerate(histogram):
    # Checks if we're entering a variable region.
    if frequency < 85 and not in_variable_region:
        in_variable_region = True
        print(base_pair_group * bin_size - bin_size * 0.5, '\t', file=output_file_handler,sep='', end='')
        variable_region_starts.append(base_pair_group * bin_size - bin_size * 0.5)
    # Checks if we're leaving a variable_region.
    elif frequency > 85 and in_variable_region:
        in_variable_region = False
        print(base_pair_group * bin_size - bin_size * 0.5, file=output_file_handler)
        variable_regions_ends.append(base_pair_group * bin_size - bin_size * 0.5)
if in_variable_region:
    in_variable_region = False
    print(base_pair_group * bin_size - bin_size * 0.5, file=output_file_handler)
    variable_regions_ends.append(base_pair_group * bin_size - bin_size * 0.5)

output_file_handler.close()




# PROBLEM 4 STARTS HERE:

def variable_region_function(x):
    domain = []
    y = []
    for x_i in x:
        in_variable_region = False
        for index in range(len(variable_region_starts)):

            if x_i >= variable_region_starts[index] and x_i <= variable_regions_ends[index]:
                y.append(graph_percentage_shown_for_variable_region)
                domain.append(x_i)
                in_variable_region = True
        if not in_variable_region:
            y.append(np.nan)
    return np.array(domain), np.array(y)

# Need to create a differnt x so that multiple points are found to connect in each variable region.
other_xlist = np.linspace(0, bin_size * len(histogram) - bin_size, num=len(histogram) * 2)

variable_region_domain, variable_region = variable_region_function(other_xlist)

plt.figure(num=1, dpi=120)
plt.plot(xlist, histogram, label="Sliding window average")
plt.plot(other_xlist, variable_region, label="Variable region")
plt.xlabel("Gene Position")
plt.ylabel("%Sequence Identity")
plt.legend()

plt.savefig("solution-problem-4.pdf", format='pdf')

plt.show()



# BONUS

input_file_name = "Homework4-seqs-with-primers.fna"
input_file_handler = open(input_file_name, "r")

seq_list = []

for line in input_file_handler:
    if line[0] == ">":
        continue

    seq_list.append(line.rstrip())
input_file_handler.close()

batch = np.random.randint(0, len(seq_list), size=100)
new_seq_list = []
for seq_index in batch:
    new_seq_list.append(seq_list[seq_index])

shortest_variable_region_index = np.argmin(np.array(variable_regions_ends) - np.array(variable_region_starts))
largest_variable_region_index = np.argmax(np.array(variable_regions_ends) - np.array(variable_region_starts))
shortest_variable_region_start = variable_region_starts[shortest_variable_region_index]
shortest_variable_region_end = variable_regions_ends[shortest_variable_region_index]
largest_variable_region_start = variable_region_starts[largest_variable_region_index]
largest_variable_region_end = variable_regions_ends[largest_variable_region_index]

batch1_output_file_name = "batch1.fna"
batch1_output_file_handler = open(batch1_output_file_name, "w")
for batch_seq in new_seq_list:
    for sequence_index, nucleotide in enumerate(batch_seq):
        if sequence_index >= largest_variable_region_start and sequence_index <= largest_variable_region_end:
            print(nucleotide, file=batch1_output_file_handler, end='')
    print("", file=batch1_output_file_handler)

batch1_output_file_handler.close()

batch2_output_file_name = "batch2.fna"
batch2_output_file_handler = open(batch2_output_file_name, "w")
for batch_seq in new_seq_list:
    for sequence_index, nucleotide in enumerate(batch_seq):
        if sequence_index >= shortest_variable_region_start and sequence_index <= shortest_variable_region_end:
            print(nucleotide, file=batch2_output_file_handler, end='')
    print("", file=batch2_output_file_handler)

batch2_output_file_handler.close()

batch3_output_file_name = "batch3.fna"
batch3_output_file_handler = open(batch3_output_file_name, "w")
for batch_seq in new_seq_list:
    print(batch_seq, file=batch3_output_file_handler)

batch3_output_file_handler.close()

# ...Now to plug this into hw3 code to get trees.
