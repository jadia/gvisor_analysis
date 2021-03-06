import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt
import csv

results = {}

# Grab data and put into dictionary
with open(sys.argv[1]) as f:
	csv_reader = csv.reader(f, delimiter=',')
	for row in csv_reader:
		if (row[0] not in results):
			results[row[0]] = {}
		if (row[1] not in results[row[0]]):
			results[row[0]][row[1]] = []
				
		results[row[0]][row[1]].append(float(row[2]))

# Calculate mean throughput for each
def throughput(data, size):
	return int(size)/(data *1000000000) # GB/s

averages = {}
for platform in results:
	if (platform not in averages):
		averages[platform] = {}

	for size in results[platform]:
		averages[platform][size] = statistics.mean(results[platform][size])

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

for platform in averages:
	averages[platform] = sort_keys(averages[platform])

if (sys.argv[2] == "bar"):
	n_groups = 5

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.1
	opacity = 0.8
	'''
	rects1 = plt.bar(index, averages['bare'], bar_width,
	alpha=opacity,
	color='0.7',
	label='bare')
	'''
	rects2 = plt.bar(index + 0*bar_width, averages['runc'], bar_width,
	hatch='-',
	alpha=opacity,
	color='0.5',
	label='runc')
	'''
	rects3 = plt.bar(index +  2*bar_width, averages['runsc_ptrace'], bar_width,
	alpha=opacity,
	color='0.7',
	label='runsc_ptrace')
	'''
	rects3 = plt.bar(index + 1*bar_width, averages['runsc_kvm'], bar_width,
	alpha=opacity,
	hatch='/',
	color='0.5',
	label='runsc_kvm')
	'''
	rects5 = plt.bar(index + 2*bar_width, averages['mod_ptrace'], bar_width,
	alpha=opacity,
	color='r',
	label='mod_ptrace')
	'''
	rects4 = plt.bar(index + 2*bar_width, averages['mod_kvm'], bar_width,
	alpha=opacity,
	color='0.2',
	label='mod_kvm')

	plt.xlabel('Read Size')
	plt.ylabel('Average Throughput (GB/Sec)')
	plt.title('Throughput of Read System Call')
	plt.xticks(index + 1.5*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))

	plt.legend(loc = 'upper left')
	 
	plt.tight_layout()

else:
	print(averages)
	plt.rc('font', family='serif')
	plt.rc('xtick', labelsize='x-small')
	plt.rc('ytick', labelsize='x-small')
	x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	fig = plt.figure(figsize=(3.5, 2.5))
	ax = fig.add_subplot(1, 1, 1)

	plt.xlabel('Concurrent Threads', fontsize=10)
	plt.ylabel('Throughput (Containers/s)', fontsize=10)
	width = 3	

	# Plot each
	plt1, = plt.plot(x, averages["runc"], color = 'gray', linewidth=width,linestyle=':')	
	plt2, = plt.plot(x, averages["ptrace"], color = 'gray', linewidth=width, linestyle='-')	
	plt3, = plt.plot(x, averages["kvm"], color = 'gray', linewidth=width, linestyle='-.')	
	plt.legend([plt1,plt2,plt3],["runc","runsc_ptrace","runsc_kvm"],loc ='lower right', frameon=False, prop={'size': 10})
	plt.ylim(bottom=0)
	plt.tight_layout()
	plt.savefig('./threading_throughput.eps', format='eps', dpi=1000)
plt.show()
