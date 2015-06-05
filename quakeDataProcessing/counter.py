__author__ = 'patrickczeczko'
import ast


file = open('slurm-170493.out')

list = ast.literal_eval(file.read())

print(len(list))

total = 0

for x in list:
    total += int(x)

print(total)