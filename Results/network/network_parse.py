
# use: python3 network_parse.py logs/experiments/execute/network_throughput/test.log


import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt
import csv
import re

results = {}
found = False
cmd = ''
TYPE = ''
count = 0
flag = False
final_time = float()
# save all commands into result

with open(sys.argv[1], 'r') as file:
	for line in file:
		if "LOG_OUTPUT: " in line:
			# print("Before splilt: " + line)
			time = line.split('average = ')[1]
			time = time.split(' seconds')[0]
			results[cmd].append(float(time))
			found = False
		if "platform" in line:
			TYPE = line.split('=')[1]
			# print("New Type: " + str(TYPE))
		if "Executing: " in line:
			cmd = line.split(': ', 1)[1] + " " + str(TYPE)
			if (cmd not in results):
				results[cmd] = []
			found = True

print(results)


# print(results)
# exit(1)


for command in results:
    print("Command: " + str(command.strip('\n')))
    for val in results[command]:
        print(val)

    print('\n')

plot_results = []

for command in results:
    # print("Command: " + str(command.strip('\n')))
    size = re.findall(r"test\d+", command)[0]
    # print(size)
    size = size.split('test')[1]
    if "runsc" in command:
        if "kvm" in command:
                plot_results.append(["runsc_kvm", size, results[command]])
        else:
                plot_results.append(["runsc_ptrace", size, results[command]])
    elif "kata" in command:
                plot_results.append(["kata", size, results[command]])    
    elif "runc" in command:
        plot_results.append(["runc", size, results[command]])
    else:
        plot_results.append(["bare", size, results[command]])
print(plot_results)
print("Open network.csv")
with open('network.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for row in plot_results:
        for i in range(0, len(row[2])):
            writer.writerow([row[0], row[1], row[2][i]])
