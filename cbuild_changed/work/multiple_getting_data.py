# Default World topology
# WORLD_X 60                  # Width of the Avida world
# WORLD_Y 60                  # Height of the Avida world
xy = {'x': 120, 'y': 120}

# python multiple_getting_data.py -f p9 

# p6 has data for 1000 updates for all 29 combinations/orderings of rewards. p7 is the same as p6 except running again so we have more data (like so we can average across multiple trieals fro the same configuration)
# 29 combinations/orderings of rewards: [[1, 2, 3, 4, 5], [1, 2, 4, 3, 5], [1, 3, 2, 4, 5], [1, 3, 4, 2, 5], [1, 4, 2, 3, 5], [1, 4, 3, 2, 5], [2, 1, 3, 4, 5], [2, 1, 4, 3, 5], [2, 3, 1, 4, 5], [2, 3, 4, 1, 5], [2, 4, 1, 3, 5], [2, 4, 3, 1, 5], [3, 1, 2, 4, 5], [3, 1, 4, 2, 5], [3, 2, 1, 4, 5], [3, 2, 4, 1, 5], [3, 4, 1, 2, 5], [3, 4, 2, 1, 5], [4, 1, 2, 3, 5], [4, 1, 3, 2, 5], [4, 2, 1, 3, 5], [4, 2, 3, 1, 5], [4, 3, 1, 2, 5], [4, 3, 2, 1, 5], [1, 2, 3, 4, 6], [1, 2, 3, 4, 4], [1, 2, 3, 4, 3], [1, 2, 3, 4, 2], [1, 2, 3, 4, 1]]

# If tasks files aren't printing counts of organisms with certain functions, then try making sure environment.cfg contains the rewards for the tasks you want to see.

# Tweak requisite:max_count in envrionment.cfg, reward values in envrionment.cfg through this file, mutation rate in avida.cfg, grid size in avida.cfg through this file, # of updates, where 10 updates are roughly equal to 1 generation, in events.cfg by EXIT.


# Look in "/Users/albertzhang/GitHub/avida/cbuild/work/data/229r/p2" to get data on how many organisms have evolved EQU and other functions by certain timesteps.

# Search for ALBERT in the whole repo to find comments in other files that I wrote as notes for how to get this code to work
# Ex: In `avida-core/source/main/cStats.cc`: // ALBERT: This is a hack to get the filename from the config file dat_filenames.txt, i pass in the stuff from the config file directly into this function via str.c_str() 

# python getting_data.py -o testing1.txt  # default command './avida' will be used
# python getting_data.py ./some-command -o testing1.txt  # 'some-command' will be executed
# ALBERT: I'm always going to run this with the command './avida' so I don't need to specify it (no other commands to run). Also, at this point I automatically name the file based on the datetime and configs, so don't need to include file name either. So can just do "python getting_data.py" and it will run the command './avida' and save the output to a file named based on the datetime and configs.
# -o filename is appended to end of log file, so still useful if you want to specifically mark some name for the logfile.
# DEFAULT_values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 3.0, 'ANDN': 3.0, 'NOR': 4.0, 'XOR': 4.0, 'EQU': 5.0}
original_values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 3.0, 'ANDN': 3.0, 'NOR': 4.0, 'XOR': 4.0, 'EQU': 5.0}
# values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 4.0, 'ANDN': 4.0, 'NOR': 5.0, 'XOR': 5.0, 'EQU': 8.0}
multiplier = 1
for val in original_values:
    original_values[val] *= multiplier


import argparse
import os
import subprocess
import time
import multiprocessing
import copy

parser = argparse.ArgumentParser(
    description="Execute a command and redirect output to a file"
)
parser.add_argument(
    "command", nargs="*", default="./avida", help="the command to execute"
)
parser.add_argument(
    "-o", "--output", metavar="FILE", help="the output file name", required=False
)


parser.add_argument(
    "-f", "--folder_name", metavar="folder_name", help="the folder_name", required=False
)

args = parser.parse_args()

def run_experiment(values, xy, max_count, folder_name = "ptest", index = 0):

    experiment_start_time_string = time.strftime(
                "%m-%d_%H-%M-%S", time.localtime(time.time())
            )

    log_file_name = f"229r/{str(folder_name)}/{index}_mxc_{str(max_count)}_" + str(values) + f"_date_{experiment_start_time_string}_xy{str(xy.values())}.txt"
    
    if args.output:
        log_file_name +=  str(args.output)
        
    # specify the directory path relative to the current working directory
    directory_path = "/".join(log_file_name.split("/")[:2])

    # get the absolute path of the directory
    absolute_path = os.path.abspath(directory_path)
    # print(absolute_path)
    
    # create the directory if it doesn't exist
    if not os.path.exists(absolute_path):
        # print(absolute_path)
        os.makedirs(absolute_path)

    with open('dat_filenames.txt', 'w') as f:
        f.write(log_file_name)

    with open('avida.cfg', 'r') as f:
        contents = f.read()
        
    vals = copy.deepcopy(original_values)
    vals["NOT"] = values[0]
    vals["NAND"] = values[0]
    vals["AND"] = values[1]
    vals["ORN"] = values[1]
    vals["OR"] = values[2]
    vals["ANDN"] = values[2]
    vals["NOR"] = values[3]
    vals["XOR"] = values[3]
    vals["EQU"] = values[4]
    values = vals

    # Modify the WORLD_X and WORLD_Y parameters in the file contents
    lines = contents.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('WORLD_X'):
            lines[i] = f"WORLD_X {xy['x']}"  
        elif line.startswith('WORLD_Y'):
            lines[i] = f"WORLD_Y {xy['y']}"  

    # Join the modified lines back together
    new_contents = '\n'.join(lines)

    # Write the modified contents back to the file
    with open('avida.cfg', 'w') as f:
        f.write(new_contents)


    with open('environment.cfg', 'r') as f:
        contents = f.read()

    # Split the contents of the file into individual lines
    lines = contents.split('\n')

    # Modify the process:value parameter for each reaction
    for i, line in enumerate(lines):
        if line.startswith('REACTION'):
            parts = line.split()
            value = float(parts[3].split('=')[1].split(':')[0])
            if f'value={value}' in line:
                lines[i] = line.replace(f'value={value}', f'value={values[parts[1]]}')
            # didn't udpate environment correctly because it was lookin for floats not ints
            elif f'value={int(value)}': 
                lines[i] = line.replace(f'value={int(value)}', f'value={values[parts[1]]}')
            else:
                raise Exception(f'Could not find value={value} in line {line}!')
            
            if max_count == -1:
                lines[i] = lines[i].replace(f'requisite:max_count=1', "")
            else:
                if "max_count=1" not in line:
                    lines[i] = lines[i] + 'requisite:max_count=1'
            
            if max_count != 1 and "EQU" in line:
                lines[i] = lines[i].replace(f'requisite:max_count=1', "")
            
    # Join the modified lines back together
    contents = '\n'.join(lines)
    
    # print(contents)

    # Write the modified contents to a new file
    with open('environment.cfg', 'w') as f:
        f.write(contents)

    with open(log_file_name, "a+") as f:
        f.write(str(values) + "\n")
        f.write(str(xy) + "\n")

    start_time = time.time()

    with open(log_file_name, "a") as f:
        result = subprocess.run(args.command, stdout=f)

    new_lines = []
    # Read data from file into a list of strings
    with open(log_file_name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            keep = True
            if line.startswith("229r/"):
                keep = False
                continue
            if line.startswith("UD:"):
                ud_value = int(line.split()[1])
                if ud_value % 100 != 0:
                    keep = False 
            if keep:
                new_lines.append(line)
                
    with open(log_file_name, "w") as f:
        for line in new_lines:
            f.write(line)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time:.3f} seconds")
    # TODO: figure out how to get Python to modify the values in environment.cfg, or have Python create a new environment.cfg file in this directory to replace the existing one, then execute the command.
    

if __name__ == '__main__':
    # All settings are default except 120 x 120 world and u 10000 Exit
    
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
        
    # print(big_list)
    
    values_list = big_list
    values_list2 = [
    [1,2,3,4,6],
    [1,2,3,4,4],
    [1,2,3,4,3],
    [1,2,3,4,2],
    [1,2,3,4,1],
    ]
    values_list = values_list2 + values_list
    
    # print(values_list)
    max_counts = [1, 0, -1]
    # TODO will need to update plotting and dataframe data to account for max_counts = [1, 0, -1] instead of max_counts = [True, False]
    # 14 is when max_counts = [1, 0, -1]
    for i in range(16,100):
        for values in values_list:
            for max_count in max_counts:
                run_experiment(values, xy = xy, folder_name=args.folder_name, max_count=max_count, index=i)
