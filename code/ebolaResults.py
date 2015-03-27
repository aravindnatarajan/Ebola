import cPickle as pickle
import numpy as np
import triangle
import os
import sys

def main(inputFolder, outputFileName, burn):
    
  inputFileNames = [inputFolder+"/"+val for val in os.listdir(inputFolder) if ".DS_Store" not in val]
  numFiles = len(inputFileNames)
  
  params = ['k', 'tControl', 'Td', 'rhoI0', 'rhoD0']
  samp3 = []; meanC = []; meanD = []
  for fileName in inputFileNames:
    print "Reading file " + fileName + " . . ."
    details = pickle.load(open(fileName))
    timeSteps = len(details['C'][0][0])            
    numChains = len(details[params[0]])    
    print "Found " + str(numChains) + " chain(s)."
    print "Discarding " + str(burn) + " chain(s)."
    print "\n"[:-1]

    print "Averaging cases and deaths over chains."
    arrayC = []; arrayD = []
    for chain in range(burn,numChains):    
      chainLength = len(details['C'][chain])    
      arrayC.append([np.mean([details['C'][chain][val][i] for val in range(0,chainLength)]) for i in range(0,timeSteps)])    
      arrayD.append([np.mean([details['D'][chain][val][i] for val in range(0,chainLength)]) for i in range(0,timeSteps)])          
    meanC.append([np.mean([arrayC[val][i] for val in range(0,numChains-burn)]) for i in range(0,timeSteps)])      
    meanD.append([np.mean([arrayD[val][i] for val in range(0,numChains-burn)]) for i in range(0,timeSteps)])            
    
    samp2 = []
    for pLoop in range(0,len(params)):
      var = params[pLoop]
      print "Reading traces for parameter: " + var
      samp1 = []
      for loop1 in range(burn,len(details[var])): 
        off = np.sum([len(details[var][lp2]) for lp2 in range(1,loop1)])
        for i in range(0,len(details[var][loop1])):
          samp1.append(details[var][loop1][i])
      samp2.append(samp1)
    samp3.append(samp2)
    print "\n"[:-1]
     
  # Average over files.   
  cases  = [np.mean([meanC[val][i] for val in range(0,numFiles)]) for i in range(0,timeSteps)]
  deaths = [np.mean([meanD[val][i] for val in range(0,numFiles)]) for i in range(0,timeSteps)]
       
  kChain = []; tControlChain = []; TdChain = []; rhoI0 = []; rhoD0 = []
  for i in range(0,len(inputFileNames)):
    kChain += samp3[i][0]
    tControlChain += samp3[i][1]
    TdChain += samp3[i][2]
    rhoI0 += samp3[i][3]
    rhoD0 += samp3[i][4]

  medianValues = [np.median(kChain), np.median(tControlChain), np.median(TdChain), np.median(rhoI0), np.median(rhoD0)]   
  stdValues = [np.std(kChain), np.std(tControlChain), np.std(TdChain), np.std(rhoI0), np.std(rhoD0)]
    
  for i in range(0,len(params)):
    print "Median value of " + str(params[i]) + " = " + str(medianValues[i]) + ", std dev = " + str(stdValues[i])

  print "\n"[:-1]           
  samples = np.array([kChain,tControlChain,TdChain,rhoI0,rhoD0]).T
  print "Number of samples: " + str(len(samples))
  print "Saving plot to file: " + outputFileName
  plt = triangle.corner(samples, labels=params, truths=medianValues)
  plt.savefig(outputFileName)
  print "\n"[:-1]
  print "Mean number of cases and deaths."
  for i in range(0,timeSteps):
    print i,cases[i],deaths[i]

if __name__ == "__main__":

  if len(sys.argv) != 3 and len(sys.argv) != 4: 
    print "Please provide a valid input folder and an output file name."
    print "e.g. python plot.py chains_folder my_plot.png"
    sys.exit()
  
  if len(sys.argv) == 4: 
    burn = int(sys.argv[3])  
    print "Setting burn = " + str(burn)    
  else:  
    print "No burn-in provided. Assuming burn = 0."
    burn = 0
  inputFileNames = os.listdir(sys.argv[1])
  if len(inputFileNames) == 0:
    print "No files found in folder."
    sys.exit()
  
  main(sys.argv[1], sys.argv[2], burn)
  