# python getting_data.py -o testing1.txt  # default command './avida' will be used
# python getting_data.py ./some-command -o testing1.txt  # 'some-command' will be executed

import argparse
import subprocess

parser = argparse.ArgumentParser(
    description="Execute a command and redirect output to a file"
)
parser.add_argument(
    "command", nargs="*", default="./avida", help="the command to execute"
)
parser.add_argument(
    "-o", "--output", metavar="FILE", help="the output file name", required=True
)

args = parser.parse_args()

with open('environment.cfg', 'r') as f:
    contents = f.read()

# Split the contents of the file into individual lines
lines = contents.split('\n')

# Create an empty dictionary to store the process:value for each reaction
processes = {}

# Loop through each line in the file
for line in lines:
    if line.startswith('REACTION'):
        parts = line.split()
        print(parts)
        value = float(parts[3].split('=')[1].split(':')[0])
        name = parts[1]
        processes[name] = value

# Print out the dictionary
print(processes)


with open('environment.cfg', 'r') as f:
    contents = f.read()

# Split the contents of the file into individual lines
lines = contents.split('\n')

# Modify the process:value parameter for each reaction
for i, line in enumerate(lines):
    if line.startswith('REACTION'):
        parts = line.split()
        value = float(parts[3].split('=')[1].split(':')[0])
        new_value = value * 2
        lines[i] = line.replace(f'value={value}', f'value={new_value}')

# Join the modified lines back together
contents = '\n'.join(lines)

# Write the modified contents to a new file
with open('new_setup.txt', 'w') as f:
    f.write(contents)


# with open(args.output, "w") as f:
#     subprocess.run(args.command, stdout=f)

# TODO: figure out how to get Python to modify the values in environment.cfg, or have Python create a new environment.cfg file in this directory to replace the existing one, then execute the command.