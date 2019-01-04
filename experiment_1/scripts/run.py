import os
import json
from subprocess import Popen

''' -----------Methods-------------------'''

def handleConfig():
	print("")
	print("Printing config.txt")
	
	with open("experiment_1/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS, READ_SIZE):
	print("Testing read throughput for " + TRIALS + " trials. Cycling from 1 to " + str(READ_SIZE) + " bytes of reading.") 

def runExperiment(TRIALS, READ_SIZE):
	# Begin invoking experiment (Does 10 experiments for each config)
	
	
	print("")
	print("Running baremetal")
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: experiment_1/experiment_materials/read " + str(TRIALS) + " " + str(exp_read))
		p = Popen(['/bin/bash', '-c',  "experiment_1/experiment_materials/read " + str(TRIALS) + " " +  str(exp_read)])
		p.wait()

	print("")
	print("Running with Docker")
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: sudo docker run --rm read " + str(TRIALS) + " " + str(exp_read))
		p = Popen(['/bin/bash', '-c',  "docker run --rm read " + str(TRIALS) + " " +  str(exp_read)])
		p.wait()
		
	print("")
	print("Running gVisor: Ptrace")
	
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=ptrace"]
	print("Writing: " + str(data))
	with open('/etc/docker/daemon.json', 'w') as outfile:
    		json.dump(data, outfile)
	
	print("Restarting Docker")
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()
	
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: sudo docker run --runtime=runsc --rm read " + str(TRIALS) + " " + str(exp_read))
		p = Popen(['/bin/bash', '-c',  "docker run --runtime=runsc --rm read " + str(TRIALS) + " " +  str(exp_read)])
		p.wait()
	
	print("")
	print("Running gVisor: KVM")
	
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=kvm"]
	print("Writing: " + str(data))
	with open('/etc/docker/daemon.json', 'w') as outfile:
    		json.dump(data, outfile)
	
	print("Restarting Docker")
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: sudo docker run --runtime=runsc --rm read " + str(TRIALS) + " " + str(exp_read))
		p = Popen(['/bin/bash', '-c',  "docker run --runtime=runsc --rm read " + str(TRIALS) + " " +  str(exp_read)])
		p.wait()


	print("Completed experiment " + str(EXP_NUM))

''' ---------------Executed Code---------------'''
EXP_NUM = 1

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

# Print config file
config = handleConfig()

TRIALS = config["trials"]
READ_SIZE = config["read_size"]

if (config["built"] != "True"):
	print("Building experiment")
	p = Popen(['/bin/bash', '-c', 'python experiment_1/scripts/build.py'])
	p.wait()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS, READ_SIZE)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, READ_SIZE)

