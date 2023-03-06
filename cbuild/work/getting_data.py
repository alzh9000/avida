# Search for ALBERT in the whole repo to find comments in other files that I wrote as notes for how to get this code to work
# Ex: In `avida-core/source/main/cStats.cc`: // ALBERT: This is a hack to get the filename from the config file dat_filenames.txt, i pass in the stuff from the config file directly into this function via str.c_str() 

# python getting_data.py -o testing1.txt  # default command './avida' will be used
# python getting_data.py ./some-command -o testing1.txt  # 'some-command' will be executed
values = {'NOT': 1.0, 'NAND': 1.0, 'AND': 2.0, 'ORN': 2.0, 'OR': 3.0, 'ANDN': 3.0, 'NOR': 4.0, 'XOR': 4.0, 'EQU': 5.0}
xy = {'x': 10, 'y': 10}

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
log_file_name = "229r/" + str(xy) +"_" + str(values) + f"_{experiment_start_time_string}.txt"

log_file_name = "229r/task_date_" + str(xy) +"_" + str(values) + f"_{experiment_start_time_string}.txt"


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

with open(log_file_name, "a") as f:
    subprocess.run(args.command, stdout=f)

# TODO: figure out how to get Python to modify the values in environment.cfg, or have Python create a new environment.cfg file in this directory to replace the existing one, then execute the command.