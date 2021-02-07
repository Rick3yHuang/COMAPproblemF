import numpy as np

# With Time Dependence
totalTime = 10
timestep = .1
numsteps = int(totalTime/timestep)
numParam = 5
numMetric = 3
parameters = np.empty((numsteps,numParam), dtype=float)
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
for i in range(0,numParam):
    parameters[0,i] = float(line.split(",")[i])
print(model)
params.close()
for i in range(1, numsteps): # These are where we would implement the time dependence of the parameters
    parameters[i,0] = parameters[i-1,0]
    parameters[i,1] = 0.99*parameters[i-1,1]
    parameters[i,2] = parameters[i-1,2] + .0001
    parameters[i,3] = 1
    parameters[i,4] *= 1.01
print("temp")
print(parameters[0])
print(parameters[numsteps-1])
metric = np.empty((numsteps, numMetric), dtype=float)
for i in range(0,numsteps):
    metric[i] = np.matmul(model, parameters[i]) #multiplying the weights matrix by the parameter vector to produce the metrics

print(metric[0])
print(metric[numsteps-1])