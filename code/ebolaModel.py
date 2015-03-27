from pymc import *
import numpy as np
import sys

from ebola import *

data = np.genfromtxt(fileName)
timesArray  = data[:,0]
casesArray  = data[:,1]
deathsArray = data[:,2]
if trnLength > 0.:
  timesArray  = timesArray[:trnLength]
  casesArray  = casesArray[:trnLength]
  deathsArray = deathsArray[:trnLength]
  
sq = lambda x: x*x

@deterministic
def eirdModel(rhoI0=rhoI0,rhoD0=rhoD0,k=k,tControl=tControl,Td=Td):

  cumCasesCalc  = casesArray[0] 
  cumDeathsCalc = deathsArray[0]
      
  deltaT = 1.    # A convenient step size, in days.
  theTimes = [val*deltaT for val in range(0,int(timesArray[-1]/deltaT)+1)]
  E = cumCasesCalc; I = cumCasesCalc; Di = cumDeathsCalc
  cumCasesArray  = []; cumDeathsArray = []
  
  ctr2 = 0
  for theTime in theTimes:    
    if theTime == timesArray[ctr2]:
      cumCasesArray.append(cumCasesCalc)
      cumDeathsArray.append(cumDeathsCalc)
      ctr2 += 1
  
    if theTime < tControl:  
      rhoI  = rhoI0; rhoD  = rhoD0      
    else: 
      rhoI  = rhoI0*np.exp(-k*(theTime-tControl))
      rhoD  = rhoD0*np.exp(-k*(theTime-tControl))

    # Update values.           
    dotE  = (rhoI*(I/Ti)) + (rhoD*(Di/Td)) - (E/Tx)
    dotI  = (E/Tx) - (I/Ti)
    dotDi = (f*I/Ti) - (Di/Ti)
    E  += (deltaT*dotE)
    I  += (deltaT*dotI)
    Di += (deltaT*dotDi)

    cumCasesCalc  += (deltaT*(E/Tx))
    cumDeathsCalc += (deltaT*(f*I/Ti))

    # Fill in the arrays corresponding to observed times.     
  return cumCasesArray,cumDeathsArray  

C = Lambda('C', lambda eirdModel=eirdModel: eirdModel[0])
D = Lambda('D', lambda eirdModel=eirdModel: eirdModel[1])

mcmcCases  = Poisson('mcmcCases',  mu=eirdModel[0], value=casesArray, observed=True)
mcmcDeaths = Poisson('mcmcDeaths', mu=eirdModel[1], value=deathsArray, observed=True)
