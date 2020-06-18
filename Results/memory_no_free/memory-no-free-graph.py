# Use: python3 network_graph.py network.csv bar


import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt
import csv

results = {}

# Grab data and put into dictionary
with open("mem-free.csv") as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if (row[0] not in results):
            results[row[0]] = {}
        if (row[1] not in results[row[0]]):
            results[row[0]][row[1]] = []
                
        results[row[0]][row[1]].append(float(row[2]))

# Calculate mean throughput for each
def throughput(data, size):
    # print("size:" + str(int(size)/1000000) + " time:" + str(data))
    # return 8*int(size)/(data *1000000) # GB/s
    # print("size:" + str(size) + " time:" + str(data))
#     return 8*int(size)/(data) # Mb/s
    return round((int(size))/(data*1000000000),2) # B/ns

averages = {}
for platform in results:
    if (platform not in averages):
        averages[platform] = {}

    for size in results[platform]:
        averages[platform][size] = throughput(statistics.mean(results[platform][size]), size)

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

for platform in averages:
        averages[platform] = sort_keys(averages[platform])


        
print(averages)

for platform in averages:
    print(platform)
    for i in range(0, len(averages[platform])):
        print(float(averages[platform][i]))
# exit(1)
if (True):
# if (sys.argv[2] == "bar"):
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
#   fig = plt.figure(figsize=(3.5, 2.5))
    fig = plt.figure(figsize=(8.5, 7.5))
    ax = fig.add_subplot(1, 1, 1)
    n_groups = 5

    # create plot
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8
    
    rects1 = plt.bar(index + 0*bar_width, averages['bare'], bar_width,
    alpha=opacity,
#   color='0.1',
    color='r',
    label='bare')

#     rects2 = plt.bar(index + 1*bar_width, averages['runc'], bar_width,
#     alpha=opacity,
#     color='g',
#     label='runc')
    
    rects2 = plt.bar(index +  1*bar_width, averages['runsc_ptrace'], bar_width,
    alpha=opacity,
    color='b',
    label='runsc_ptrace')
    
    rects3 = plt.bar(index + 2*bar_width, averages['runsc_kvm'], bar_width,
    alpha=opacity,
    color='m',
    label='runsc_kvm')

    rects4 = plt.bar(index + 3*bar_width, averages['kata'], bar_width,
    alpha=opacity,
    color='k',
    label='kata')

    plt.xlabel('Malloc Size', fontsize=10)
    plt.ylabel('Throughput (MBps)', fontsize=10)
    plt.xticks(index + 2*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))
    plt.xlim(left=-2*bar_width)
    plt.legend(loc = 'upper right')
    plt.legend(loc = 'upper right', frameon=False, prop={'size':10})
    ax.tick_params(axis=u'both', which=u'both',length=0)     
    plt.tight_layout()
    plt.savefig('./memory_throughput.png', format='png', dpi=1000)
plt.show()