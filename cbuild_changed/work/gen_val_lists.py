# Create a list of values to pass to the function
from itertools import permutations

lst = [1, 2, 3, 4]

# Generate all permutations of the list
perms = permutations(lst)

big_list = []
# Print all permutations
for perm in perms:
    big_list.append(list(perm))
for list in big_list:
    list += [5]
    
print(big_list)
