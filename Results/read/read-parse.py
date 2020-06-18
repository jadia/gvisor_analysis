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
        if "platform" in line:
            TYPE = line.split('=')[1]
        if "Executing: " in line:
            cmd = line.split(': ', 1)[1] + " " + str(TYPE)
            if (cmd not in results):
                results[cmd] = []
            print(cmd)
            # exit(1)
        if "LOG_OUTPUT: " in line:
            time = line.split('average = ')[1]
            time = time.split(' seconds')[0]
            results[cmd].append(float(time))

# print(results)


# print(results)
# exit(1)


# for command in results:
#     print("Command: " + str(command.strip('\n')))
#     for val in results[command]:
#         print(val)

#     print('\n')

plot_results = []

for command in results:
    # print("Command: " + str(command.strip('\n')))
    num_array = re.findall(r"[-+]?\d*\.\d+|\d+", command)
    size = num_array[-1]
    # size = re.findall(r"test\d+", command)[0]
    # print(size)
    # size = size.split('test')[1]
    print(command)
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
# print(plot_results)
print("Open read.csv")
with open('read.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for row in plot_results:
        for i in range(0, len(row[2])):
            writer.writerow([row[0], row[1], row[2][i]])
