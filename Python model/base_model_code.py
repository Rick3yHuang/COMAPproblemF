import numpy as np

numParam = 11
numMetric = 6

#Without Time dependence
parameters = np.empty(numParam, dtype=float)
model = np.empty((numMetric,numParam), dtype=float)
weights = open("weights.csv", "r")
for count, line in enumerate(weights): # reading in the model weights from a csv file
    line = line.split(',')
    for num in range(0,len(line)):
        model[count, num] = float(line[num])
weights.close()
params = open("parameters.csv", "r") # reading in the initial parameters from a csv file
line = params.readline()
for i in range(0,numParam):
    parameters[i] = float(line.split(",")[i])
print(model)
params.close()
metric = np.matmul(model, parameters) #multiplying the weights matrix by the parameter vector to produce the metrics
print(metric)

metricWeights = np.array([.266, .1951, .1373, .0858, .0509, .0481])
ESH = np.dot(metricWeights, metric)
print(ESH)

