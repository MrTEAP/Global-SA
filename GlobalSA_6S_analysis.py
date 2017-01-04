from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import Py6S
import datetime
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
import multiprocessing
import glob

startTime = time.time()

#print(multiprocessing.cpu_count())

######################### Define the model inputs #########################
inDataLS5 = "reflResults/LS5_GlobalSA.txt"
resultOutputFileLS5 = "LS5_ResultOutput.csv"
inDataLS7 = "reflResults/LS7_GlobalSA.txt"
resultOutputFileLS7 = "LS7_ResultOutput.csv"
inDataLS8 = "reflResults/LS8_GlobalSA.txt"
resultOutputFileLS8 = "LS8_ResultOutput.csv"
inDataSen2 = "reflResults/Sen2_GlobalSA.txt"
resultOutputFileSen2 = "Sen2_ResultOutput.csv"

problem = {
    'num_vars': 5,
    'names': ['AOT', 'Alt', 'WV', 'Oz', 'VA'],
    'bounds': [[0, 1],
               [0, 1.5],
               [0, 4.5],
               [0.25, 0.45],
               [-20, 20]]
}

runs = [[inDataLS5, resultOutputFileLS5],
        [inDataLS7, resultOutputFileLS7],
        [inDataLS8, resultOutputFileLS8],
        [inDataSen2, resultOutputFileSen2]]

S1 = []
S1_conf = []
S2 = []
S2_conf = []
ST = []
ST_conf = []
param_name = ('AOD','Alt','WV','Oz','VA')

count = 0
######################### Generate samples #########################
N = []
inFile = np.loadtxt("reflResults/LS5_GlobalSA.txt", float)
N.append(len(inFile)/12)
N = int(N[0])
param_values = saltelli.sample(problem, N, calc_second_order=True)
totalVar = N*12

######################### Perform analysis #########################
for run in runs:
    inputFile = run[0]
    resultOutputFile = run[1]
    inFile = np.loadtxt(inputFile, float)
    for i in range(6):
        outputfiletranspose = np.transpose(inFile)
        Y = outputfiletranspose[i]
        Si = sobol.analyze(problem, Y)
        S1.append(Si['S1'])
        S1_conf.append(Si['S1_conf'])
        S2.append(Si['S2'])
        S2_conf.append(Si['S2_conf'])
        ST.append(Si['ST'])
        ST_conf.append(Si['ST_conf'])
    
    ######################### Output analysis #########################
    file = open(resultOutputFile, "w")
    file.write(",AOD,Alt,WV,Oz,VA" + "\n")
    for i in range(5):
        file.write(param_name[i])
        for j in range(5):
            file.write("," + str(Si['S2'][i,j]))
        file.write("\n")
    file.close()
    
    count = count + 1

"""
# Print the sensitivity indices
print('S1 =', Si['S1'])
print('S1 confidence =', Si['S1_conf'])
print('S2 =', Si['S2'])
print('S2 confidence =', Si['S2_conf'])
print('ST =', Si['ST'])
print('ST confidence =', Si['ST_conf'])
"""

endTime = time.time() - startTime
print('Time taken:', endTime)
