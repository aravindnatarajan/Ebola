 import matplotlib.pyplot as plt
import pymc
import sys
import os 
import numpy as np
import ebolaModel as ebolaModel
import ebola as ebola

def main():

  data = np.genfromtxt(ebola.fileName)
  paramsArray = [ebolaModel.rhoI0,ebolaModel.rhoD0,ebolaModel.k,ebolaModel.tControl,ebolaModel.Td]
  files = os.listdir(ebola.outFolderName)
  print "Setting numSamples = " + str(ebola.numSamples)
  print "Burn-in = " + str(ebola.numBurn)
  if ebola.output not in files:
    print "Creating file " + ebola.output + " in folder " + ebola.outFolderName
    M = pymc.MCMC(ebolaModel, db="pickle", dbname=ebola.outFolderName+"/"+ebola.output)
    M.use_step_method(pymc.AdaptiveMetropolis, paramsArray)
    M.sample(iter=ebola.numSamples,burn=ebola.numBurn,verbose=1)
    #pymc.Matplot.plot(M)    

  else:
    print "Reading file " + ebola.output + " in folder " + ebola.outFolderName
    db = pymc.database.pickle.load(ebola.outFolderName+"/"+ebola.output)
    dbM = pymc.MCMC(ebolaModel,db=db)
    dbM.sample(iter=ebola.numSamples,burn=ebola.numBurn,verbose=1)
    dbM.db.commit()
    dbM.db.close()
    #pymc.Matplot.plot(dbM)    

  plt.plot(data[:,1], 'C', mec='black', color='black', alpha=.9)
  plt.plot(ebolaModel.C.stats()['mean'], color='red', linewidth=2)
  plt.plot(ebolaModel.C.stats()['95% HPD interval'], color='red',linewidth=1, linestyle='dotted') 
  plt.show()


if __name__ == "__main__":
  main()
      