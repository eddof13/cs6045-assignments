import csv
import sys
from collections import defaultdict

# Wagner-Fischer algorithm (DP implementation to calculate Levenshtein distance)
# distance(s, t):
#   m = length of s
#   n = length of t
#   initialize matrix of m+1 * n+1
#   initialize all values to 0
#   set source prefixes for each word transforming to empty
#   d[i, 0] = i for i from 1 to m
#   set target prefixes for each word starting from empty
#   d[0, j] = j for j from 1 to n
#   for j from 1 to n:
#     for i from 1 to m:
#       if s[i] == t[j], cost = 0
#       else cost = 1
#       d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + cost # deletion, insertion, substitution
#   return d[m, n]

def distance(first, second):
    # matrix is 0 indexed, words are 1 indexed (in the algorithm)
    dist = defaultdict(lambda: 0)
    for i in range(1, len(first) + 1):
        dist[f'{i},0'] = i
    for j in range(1, len(second) + 1):
        dist[f'0,{j}'] = i
    for j in range(1, len(second) + 1):
        for i in range(1, len(first) + 1):
            if first[i - 1] == second[j - 1]:
                cost = 0
            else:
                cost = 1
            dist[f'{i},{j}'] = min([dist[f'{i-1},{j}'] + 1, dist[f'{i},{j-1}'] + 1, dist[f'{i-1},{j-1}'] + cost])
    return dist[f'{len(first)},{len(second)}']

def words(input_file):
    with open(input_file, "r") as file:
        reader = csv.reader(file)
        words = [[row[0].strip(), row[1].strip()] for row in reader]
    return words

if len(sys.argv) < 3:
    print("EXPECTED: python assignment_3.py INPUT_FILE OUTPUT_FILE")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
with open(output_file, "w") as file:
    for pair in words(input_file):
        file.write(f'{pair[0]}, {pair[1]}, {distance(pair[0], pair[1])}\n')
print("Output has been successfully written to", output_file)
