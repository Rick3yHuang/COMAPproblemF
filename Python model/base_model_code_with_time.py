import numpy as np
import matplotlib.pyplot as plt
import random


def show_status(year):
    outfile.write("Parameters at year " + str(year) + "\n")
    outfile.write(str(parameters[int((year/timestep))]) + "\n")
    outfile.write("Metrics at year " + str(year) + "\n")
    outfile.write(str(metric[int((year/timestep))]) + "\n")
    outfile.write("ESH at year " + str(year) + "\n")
    outfile.write(str(ESH[int((year/timestep))]) + "\n")
    outfile.write(str(year) + " year sustainability: " + "\n")
    outfile.write(str(sustainability[int((year/timestep))]) + "\n")
    outfile.write("---\n")


runName = "US 2016"
# With Time Dependence
totalTime = 10
timestep = .1
numsteps = int(totalTime/timestep)+1
numParam = 11
numMetric = 6
parameters = np.empty((numsteps,numParam), dtype=float)
#for i in range(0,numParam):
#    parameters[0,i] = 5*random.random()
model = np.empty((numMetric,numParam), dtype=float)
weights = open("weights.csv", "r")
for count, line in enumerate(weights): # reading in the model weights from a csv file
    line = line.split(',')
    for num in range(0,len(line)):
        model[count, num] = float(line[num])
weights.flush()
weights.close()
params = open("parameters.csv", "r") # reading in the initial parameters from a csv file
line = params.readline()
scales = open("Variable Scaling.csv", "r")
scales.readline()
for i in range(0,numParam):
    parameters[0,i] = float(line.split(",")[i])*float(scales.readline().split(",")[1])
params.close()
scales.close()
metricWeights = np.array([.266, .1951, .1373, .0858, .0509, .0481])
ESH = np.empty(numsteps)

timeDependence = np.zeros(numParam)

#Default time dependencies for parameters
timeDependence[2] += .01
timeDependence[4] += .01
timeDependence[9] += .03

#The following are potential education policies, simply toggle True/False to turn them On/Off
#increase in research funding
if False:
    timeDependence[6] += .02
    timeDependence[7] += .02

#make it easier for intl students to attend schools
if False:
    timeDependence[5] += .02
    timeDependence[2] += .01

#increase domestic scholarship funding
if False:
    timeDependence[0] -= .02
    timeDependence[1] -= .02
    timeDependence[2] += .02

#increase teacher pay
if False:
    timeDependence[1] += .02
    timeDependence[0] += .01

#opening more schools
if False:
    timeDependence[2] -= .02

for i in range(1, numsteps): # These are where we would implement the time dependence of the parameters
    parameters[i,0] = parameters[i-1,0] * (1+timeDependence[0]*timestep) #Variable INCOME
    parameters[i,1] = parameters[i-1,1] * (1+timeDependence[1]*timestep) #Variable STUDENT/TEACHER RATIO
    parameters[i,2] = parameters[i-1,2] * (1+timeDependence[2]*timestep) #Variable SCHOOL SIZE
    parameters[i,3] = parameters[i-1,3] * (1+timeDependence[3]*timestep) #Fixed INCOME
    parameters[i,4] = parameters[i-1,4] * (1+timeDependence[4]*timestep) #Fixed COUNTRY POPULATION
    parameters[i,5] = parameters[i-1,5] * (1+timeDependence[5]*timestep) #Variable INTL STUDENT PERCENT
    parameters[i,6] = parameters[i-1,6] * (1+timeDependence[6]*timestep) #Variable RESEARCH (TIMES)
    parameters[i,7] = parameters[i-1,7] * (1+timeDependence[7]*timestep) #Variable CITATION (TIMES)
    parameters[i,8] = parameters[i-1,8] * (1+timeDependence[8]*timestep) #Fixed MALE/FEMALE RATIO
    parameters[i,9] = parameters[i-1,9] * (1+timeDependence[9]*timestep) #Fixed COUNTRY GDP
    parameters[i,10] = parameters[i-1,10] * (1+timeDependence[10]*timestep) #Fixed # OF NOBEL PRIZE WINNERS
metric = np.empty((numsteps, numMetric), dtype=float)
for i in range(0,numsteps):
    metric[i] = np.matmul(model, parameters[i]) #multiplying the weights matrix by the parameter vector to produce the metrics
    ESH[i] = np.dot(metricWeights, metric[i])

sustainability = np.zeros(numsteps)
for i in range(1,numsteps):
    sustainability[i] = (ESH[i] - ESH[0])/ESH[0]

outfile = open("outputs.txt","a+")
outfile.write("\n" + runName + "\n")
outfile.write("~~~~~~~~~~~~~~~~~~~~\n")
show_status(0)
show_status(5)
show_status(10)

# sus3 = False
# sus10 = False
# # Health after 3 years
# if (abs(ESH[0] - ESH[int(3/timestep)-1])) < ESH[0]*.1:
#     sus3 = True
#
# # Health after 10 years
# if (abs(ESH[0] - ESH[int(10/timestep)-1])) < ESH[0]*.1:
#     sus10 = True
#
#
# if sus3:
#     print("Sustainable for 3 years")
# else:
#     print("Not sustainable for 3 years")
#
# if sus10:
#     print("sustainable for 10 years")
# else:
#     print("Not sustainable for 10 years")

time = np.linspace(0, totalTime, num=numsteps)
plt.plot(time, ESH)
plt.ylabel("Education System Health Index")
plt.xlabel("Time (years)")
plt.title("Country ESH Over Time")
plt.show()
