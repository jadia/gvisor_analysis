import os
import sys
import json
from subprocess import Popen

''' -----------Methods-------------------'''

def flush():
	sys.stdout.flush()
	sys.stderr.flush()

def processArgs():
	return sys.argv

def handleConfig(path):
	print("")
	print("Printing config.txt")
	
	with open(str(path) + "/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS, READ_SIZE):
	print("Testing read throughput for " + TRIALS + " trials. Cycling from 1 to " + str(READ_SIZE) + " bytes of reading.") 

def runExperiment(TRIALS, READ_SIZE, path, log):
	# Begin invoking experiment (Does 10 experiments for each config)
	
	
	print("")
	print("Running baremetal")
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: " + str(path) + "/experiment_materials/read " + str(TRIALS) + " " + str(exp_read) + " " + str(path) + "/experiment_materials/file.txt")
		flush()
		p = Popen(['/bin/bash', '-c',  str(path) + "/experiment_materials/read " + str(TRIALS) + " " +  str(exp_read) + " " + str(path) + "/experiment_materials/file.txt"], stdout = log)
		p.wait()

	print("")
	print("Running with Docker")
		
	runDockerContainer("", READ_SIZE, TRIALS)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", READ_SIZE, TRIALS)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", READ_SIZE, TRIALS)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, READ_SIZE, TRIALS):
	for i in range(0, 10):
		exp_read = (int(READ_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: sudo docker run " + str(runtime) + " --rm --tmpfs /myapp read " + str(TRIALS) + " " + str(exp_read) + " ./file.txt")
		flush()
		p = Popen(['/bin/bash', '-c',  "docker run " + str(runtime) + " --rm --tmpfs /myapp read " + str(TRIALS) + " " +  str(exp_read) + " ./file.txt"])
		p.wait()

def modifyDockerConfig(platform):
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=" + str(platform)]
	print("Writing: " + str(data))
	with open('/etc/docker/daemon.json', 'w') as outfile:
    		json.dump(data, outfile)
	
	flush()
	
	print("Restarting Docker")
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()

	flush()

''' ---------------Executed Code---------------'''
EXP_NUM = 1

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())


#Process Arguments
args = processArgs()
path = args[1]

log = open(str(sys.argv[2]), "a+")

# Print config file
config = handleConfig(path)

TRIALS = config["trials"]
READ_SIZE = config["read_size"]

if (config["built"] != "True"):
	print("Building experiment")
	p = Popen(['/bin/bash', '-c', 'python ' + str(path) + '/scripts/build.py ' + str(path) + " " + str(sys.argv[2])], stdout = log, stderr = log)
	p.wait()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS, READ_SIZE)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

flush()

runExperiment(TRIALS, READ_SIZE, path, log)

