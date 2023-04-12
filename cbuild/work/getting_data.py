# Tweak requisite:max_count in envrionment.cfg, reward values in envrionment.cfg through this file, mutation rate in avida.cfg, grid size in avida.cfg through this file, # of updates, where 10 updates are roughly equal to 1 generation, in events.cfg by EXIT.


# Look in "/Users/albertzhang/GitHub/avida/cbuild/work/data/229r/p2" to get data on how many organisms have evolved EQU and other functions by certain timesteps.

# Search for ALBERT in the whole repo to find comments in other files that I wrote as notes for how to get this code to work
# Ex: In `avida-core/source/main/cStats.cc`: // ALBERT: This is a hack to get the filename from the config file dat_filenames.txt, i pass in the stuff from the config file directly into this function via str.c_str() 

# python getting_data.py -o testing1.txt  # default command './avida' will be used
# python getting_data.py ./some-command -o testing1.txt  # 'some-command' will be executed
# ALBERT: I'm always going to run this with the command './avida' so I don't need to specify it (no other commands to run). Also, at this point I automatically name the file based on the datetime and configs, so don't need to include file name either. So can just do "python getting_data.py" and it will run the command './avida' and save the output to a file named based on the datetime and configs.
# -o filename is appended to end of log file, so still useful if you want to specifically mark some name for the logfile.
# DEFAULT_values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 3.0, 'ANDN': 3.0, 'NOR': 4.0, 'XOR': 4.0, 'EQU': 5.0}
values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 3.0, 'ANDN': 3.0, 'NOR': 4.0, 'XOR': 4.0, 'EQU': 5.0}
# values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 4.0, 'ANDN': 4.0, 'NOR': 5.0, 'XOR': 5.0, 'EQU': 8.0}
multiplier = 1
for val in values:
    values[val] *= multiplier

# Default World topology
# WORLD_X 60                  # Width of the Avida world
# WORLD_Y 60                  # Height of the Avida world
xy = {'x': 120, 'y': 120}

import argparse
import subprocess
import time

parser = argparse.ArgumentParser(
    description="Execute a command and redirect output to a file"
)
parser.add_argument(
    "command", nargs="*", default="./avida", help="the command to execute"
)
parser.add_argument(
    "-o", "--output", metavar="FILE", help="the output file name", required=False
)

args = parser.parse_args()

experiment_start_time_string = time.strftime(
            "%m-%d_%H-%M-%S", time.localtime(time.time())
        )

log_file_name = "229r/p2/task_" + str(xy) +"_" + str(values) + f"_date_{experiment_start_time_string}.txt"
if args.output:
    log_file_name +=  str(args.output)

with open('dat_filenames.txt', 'w') as f:
    f.write(log_file_name)

with open('avida.cfg', 'r') as f:
    contents = f.read()

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
        lines[i] = line.replace(f'value={value}', f'value={values[parts[1]]}')

# Join the modified lines back together
contents = '\n'.join(lines)

# Write the modified contents to a new file
with open('environment.cfg', 'w') as f:
    f.write(contents)

with open(log_file_name, "a") as f:
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