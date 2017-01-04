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
import shutil
import os

startTime = time.time()

#print(multiprocessing.cpu_count())

######################### Define the model inputs #########################
problem = {
    'num_vars': 5,
    'names': ['AOT', 'Alt', 'WV', 'Oz', 'VA'],
    'bounds': [[0, 1],
               [0, 1.5],
               [0, 4.5],
               [0.25, 0.45],
               [-20, 20]]
}

# LS8
pxlRadValLS8 = [10, 10, 10, 10, 10, 10, 1]

# LS5
pxlRadValLS5 = [10, 10, 10, 10, 10, 1]

# LS7
pxlRadValLS7 = [10, 10, 10, 10, 10, 1]

# Sentinel2
pxlRadValSen2 = [10, 10, 10, 10, 10, 1]

lonCentre = -3.88608
latCentre = 50.68166
acquisitionTime = datetime.datetime(int(2003), int(8), int(19), int(10), int(54), int(15))
aeroProf = Py6S.AeroProfile.Maritime
atmosProf = Py6S.AtmosProfile.MidlatitudeSummer

######################### Generate samples #########################
N = 10000
param_values_array = saltelli.sample(problem, N, calc_second_order=True)
totalVar = N*12
param_values_list = []
for i in range(totalVar):
    param_values_list.append([param_values_array[i], "Run_" + str(i) + ".txt"])

param_values_file = open("param_values.txt", "w")
for i in param_values_list:
    param_values_file.write(str(i) + "\n")
param_values_file.close()

######################### Run model #########################
wvlensLS5 = [Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B1),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B2),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B3),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B4),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B5),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_TM_B7)]
outResultFileLS5 = "reflResults/LS5_GlobalSA.txt"

wvlensLS7 = [Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B1),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B2),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B3),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B4),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B5),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_ETM_B7)]
outResultFileLS7 = "reflResults/LS7_GlobalSA.txt"

wvlensLS8 = [Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B2),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B3),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B4),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B5),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B6),
             Py6S.Wavelength(Py6S.SixSHelpers.PredefinedWavelengths.LANDSAT_OLI_B7)]
outResultFileLS8 = "reflResults/LS8_GlobalSA.txt"

wvlensSen2 = [Py6S.Wavelength(0.440, 0.535, [0.001206, 0.002623, 0.002076, 0.002224, 0.002377, 0.002856, 0.009028, 0.038955, 0.292197, 0.382418, 0.400158, 0.424686, 0.505323, 0.529543, 0.534656, 0.543691, 0.601967, 0.621092, 0.575863, 0.546131, 0.571684, 0.633236, 0.738396, 0.768325, 0.788363, 0.809151, 0.844983, 0.840111, 0.78694, 0.761923, 0.810031, 0.901671, 1.0, 0.908308, 0.286992, 0.102833, 0.02508, 0.002585, 0.000441]),
              Py6S.Wavelength(0.5375, 0.5825, [0.00084, 0.080665, 0.341374, 0.828036, 0.888565, 0.860271, 0.834035, 0.867734, 0.933938, 1.0, 0.981107, 0.868656, 0.81291, 0.789606, 0.830458, 0.85799, 0.62498, 0.098293, 0.016512]),
              Py6S.Wavelength(0.6475, 0.6825, [0.034529, 0.817746, 0.983869, 0.995449, 0.977215, 0.814166, 0.764864, 0.830828, 0.883581, 0.955931, 0.973219, 0.965712, 0.944811, 0.422967, 0.063172]),
              Py6S.Wavelength(0.775, 0.9075, [0.019072, 0.056536, 0.203436, 0.450085, 0.81829, 0.960732, 0.985213, 0.93655, 0.941281, 0.962183, 0.959009, 0.945147, 0.945357, 0.937084, 0.900979, 0.86216, 0.801819, 0.755632, 0.708669, 0.690211, 0.682649, 0.67595, 0.660812, 0.65831, 0.685501, 0.720686, 0.776608, 0.78772, 0.776161, 0.759264, 0.720589, 0.69087, 0.649339, 0.627424, 0.604322, 0.591724, 0.581202, 0.580197, 0.589481, 0.596749, 0.605476, 0.613463, 0.637436, 0.659233, 0.659924, 0.615841, 0.526407, 0.49653, 0.529093, 0.537964, 0.326791, 0.14854, 0.033246, 0.007848]),
              Py6S.Wavelength(1.540, 1.6825, [7.00E-06, 2.80E-05, 0.000147, 0.00048, 0.000911, 0.001684, 0.005345, 0.012628, 0.039584, 0.07493, 0.182597, 0.330736, 0.647173, 0.815215, 0.88703, 0.891417, 0.916528, 0.935322, 0.951416, 0.956429, 0.96348, 0.96818, 0.975915, 0.979878, 0.981412, 0.980705, 0.982736, 0.987807, 0.993288, 0.990405, 0.980023, 0.972568, 0.966371, 0.96605, 0.973463, 0.983472, 0.995476, 0.998568, 0.998804, 0.99973, 0.999814, 0.99162, 0.969903, 0.953287, 0.938586, 0.928114, 0.82498, 0.641891, 0.32371, 0.163972, 0.046194, 0.019359, 0.006523, 0.003409, 0.001423, 0.000498, 3.40E-05, 1.30E-05]),
              Py6S.Wavelength(2.080, 2.320, [0.002885, 0.006597, 0.00854, 0.010002, 0.013364, 0.017126, 0.027668, 0.040217, 0.073175, 0.11147, 0.203461, 0.284898, 0.408003, 0.476537, 0.543352, 0.568634, 0.598891, 0.621362, 0.663707, 0.696165, 0.741301, 0.772071, 0.809677, 0.828599, 0.851107, 0.854746, 0.859532, 0.863257, 0.869696, 0.878588, 0.889473, 0.896696, 0.904831, 0.905665, 0.904783, 0.903347, 0.901983, 0.904313, 0.908092, 0.91295, 0.921302, 0.927219, 0.934142, 0.937086, 0.937652, 0.942518, 0.942117, 0.938428, 0.933022, 0.921057, 0.908293, 0.908191, 0.922855, 0.919482, 0.924526, 0.931974, 0.946802, 0.954437, 0.962539, 0.966042, 0.96546, 0.963656, 0.957327, 0.953558, 0.951731, 0.952641, 0.960639, 0.968307, 0.982898, 0.990734, 0.998753, 0.999927, 0.993884, 0.983735, 0.958343, 0.938203, 0.905999, 0.881683, 0.84062, 0.809516, 0.749107, 0.688185, 0.566031, 0.474659, 0.342092, 0.263176, 0.16809, 0.124831, 0.082363, 0.062691, 0.042864, 0.034947, 0.027418, 0.023959, 0.016331, 0.007379, 0.002065])]
outResultFileSen2 = "reflResults/Sen2_GlobalSA.txt"

runs = [[pxlRadValLS5, wvlensLS5, outResultFileLS5],
        [pxlRadValLS7, wvlensLS7, outResultFileLS7],
        [pxlRadValLS8, wvlensLS8, outResultFileLS8],
        [pxlRadValSen2, wvlensSen2, outResultFileSen2]]

sat = ['LS5','LS7', 'LS8','Sen2']
count = 0
S1 = []
S1_conf = []
S2 = []
S2_conf = []
ST = []
ST_conf = []
param_name = ('AOD','Alt','WV','Oz','VA')

######################### Run 6S #########################

for run in runs:
    pxlRadVal = run[0]
    wvlens = run[1]
    outResultFile = run[2]
    
    numOutVals = totalVar
    numWvLens = len(wvlens)
    
    #create empty array of output reflectance pixel values.
    outReflPxlVals = np.zeros((numWvLens, numOutVals), dtype=np.float32)

    counter = [1]
    
    def SixSf(Z):
        row_num = Z[1]
        row_num = row_num.replace("Run_","")
        row_num = row_num.replace(".txt","")
        row_num = int(row_num) + 1
        print("Processing for " + sat[count] + " param_values row " + str(row_num) + "/" + str(totalVar))
        X = Z[0]
        AOT = X[0]
        Alt = X[1]
        WV = X[2]
        Oz = X[3]
        VA = X[4]
        
        
        # Set up 6S model
        s = Py6S.SixS()
        s.atmos_profile = Py6S.AtmosProfile.PredefinedType(Py6S.AtmosProfile.MidlatitudeSummer)
        s.aero_profile = Py6S.AeroProfile.PredefinedType(Py6S.AeroProfile.Maritime)
        s.ground_reflectance = Py6S.GroundReflectance.HomogeneousLambertian(Py6S.GroundReflectance.GreenVegetation)
        s.geometry.month = acquisitionTime.month
        s.geometry.day = acquisitionTime.day
        s.geometry.gmt_decimal_hour = float(acquisitionTime.hour) + float(acquisitionTime.minute)/60.0
        s.geometry.latitude = latCentre
        s.geometry.longitude = lonCentre
        s.altitudes = Py6S.Altitudes()
        s.altitudes.set_target_custom_altitude(Alt)
        s.altitudes.set_sensor_satellite_level()
        s.atmos_corr = Py6S.AtmosCorr.AtmosCorrLambertianFromRadiance(200)
        s.aot550 = AOT
        s.atmos_profile = Py6S.AtmosProfile.UserWaterAndOzone(WV, Oz)
        s.geometry = Py6S.Geometry.User()
        s.geometry.solar_z = 46.96057185
        s.geometry.solar_a = 154.63231999
        s.geometry.view_z = VA
        s.geometry.view_a = 0
        
        wvN = 0
        varN = 0
        holder = []
        for wvlen in wvlens:
            s.wavelength = wvlen
            s.run()
            a = float(s.outputs.values['coef_xa'])
            b = float(s.outputs.values['coef_xb'])
            c = float(s.outputs.values['coef_xc'])
            y = a*pxlRadVal[wvN]-b
            holder.append((y / (1 + c * y))*100)
            wvN = wvN + 1
        
        name = str("data_storage/" + sat[count] + "/" + Z[1])
        file = open(name, "w")
        file.write(str(holder))
        file.close()
        counter.append(1)
        
        varN = varN + 1
    
        #print(outReflPxlVals)
    
    with Pool() as p:
        p.map(SixSf, param_values_list)

    ######################### Load in data files #########################
    outResults = np.zeros((totalVar,6), dtype=np.float32)
    inFiles = glob.glob("data_storage/" + sat[count] + "/*.txt")
    for file in inFiles:
        open_file = open(file, "r+")
        data_file = open_file.read()
        index = file.replace("data_storage/" + sat[count] + "/Run_","")
        index = index.replace(".txt","")
        index = int(index)
        data_file = eval(data_file)
        outResults[index] = data_file
    np.savetxt(outResultFile, outResults)

    count = count + 1

endTime = time.time() - startTime
print('Time taken:', endTime)



"""
    ######################### Perform analysis #########################
    for i in range(6):
        outputfiletranspose = np.transpose(outResults[i])
        Y = outResults[i]
        Si = sobol.analyze(problem, Y, print_to_console=False)
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
    
    #output results into a CSV file
    file = open(outResultFile, "w")
    
    #create titles
    file.write("VarValues (AOT Alt WV Oz VA)" + ",")
    for i in range(numWvLens):
        file.write("B" + str(i+1)+ ",")
    file.write("\n")
    
    #fill in coloumns with data
    for i in range(numOutVals):
        file.write("param_values")
        for j in range (numWvLens):
            file.write("," + str(outReflPxlVals[j,i]))
        file.write("\n")
    file.close()
    



# Print the sensitivity indices
print('S1 =', Si['S1'])
print('S1 confidence =', Si['S1_conf'])
print('S2 =', Si['S2'])
print('S2 confidence =', Si['S2_conf'])
print('ST =', Si['ST'])
print('ST confidence =', Si['ST_conf'])
"""
