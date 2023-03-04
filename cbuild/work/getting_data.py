import subprocess

command = ["./avida"]
output_file = "testing1.txt"

with open(output_file, "w") as f:
    subprocess.run(command, stdout=f)
