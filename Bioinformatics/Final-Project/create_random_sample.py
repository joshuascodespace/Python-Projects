import numpy as np
import sys

def ReLu(x, threshhold=0):
    y = []
    for x_i in x:
        if x_i > threshhold:
            y.append(x_i)
        else:
            y.append(0)
    return y
        
n_species = int(sys.argv[1])
n_samples = int(sys.argv[2])
output_file_name = sys.argv[3]
samples = []

for sample in range(n_samples):
    random_numbers = np.random.normal(0, 1, n_species)
    relu_random_numbers = ReLu(random_numbers)
    normalization_factor = sum(relu_random_numbers)
    for index in range(len(relu_random_numbers)):
        relu_random_numbers[index] /= normalization_factor
    samples.append(relu_random_numbers)

output_file_handler = open(output_file_name, 'w')

for sample in range(n_species):
    print(sample + 1, file=output_file_handler, end='\t')

print('', file=output_file_handler)
for sample in samples:
    for count in sample:
        print(count, file=output_file_handler, end='\t')
    print('', file=output_file_handler)
output_file_handler.close()