input_file_name = "Homework4-seqs-with-primers.fna"
input_file_handler = open(input_file_name, "r")

seq_list = []

for line in input_file_handler:
    if line[0] == ">":
        continue

    seq_list.append(line.rstrip())
input_file_handler.close()

n = len(seq_list)
m = len(seq_list[0])
valid_bases = {'A', 'C', 'G', 'T'}
identity_values = []

output_file_name = "solution-problem-1.txt"
output_file_handler = open(output_file_name, "w")

for base in range(m):
    base_counts = {}

    for seq in seq_list:
        current_nucleotide = seq[base]
        if current_nucleotide in valid_bases:
            if current_nucleotide in base_counts:
                base_counts[current_nucleotide] += 1
            else:
                base_counts[current_nucleotide] = 1
    
    # Takes the largest count of all the bases and stores it as identity value.
    identity_values.append(max(base_counts.values()))

for identity_value in identity_values:
    print(100 * identity_value / n, file=output_file_handler)

output_file_handler.close()

