
import numpy as np
import sys

sq = lambda x: x*x

def eirdModel(Tx,Ti,f,c0,d0,rhoI0,rhoD0,k,tControl,Td,tMax,tS):
    
  deltaT = 0.1    # A convenient step size, in days.
  theTimes = [int(tS) + val*deltaT for val in range(0,int((tMax-tS)/deltaT))]

  # Cases and deaths, better time resolution. 
  # Number of infected and dead. 
  cumCasesCalc  = c0; cumDeathsCalc = d0
  cumCasesArray = []; cumDeathsArray = []
  cDotArray = []; dDotArray = []
  E = cumCasesCalc; I = cumCasesCalc; Di = cumDeathsCalc
  
  for theTime in theTimes:      
    cumCasesArray.append(cumCasesCalc)
    cumDeathsArray.append(cumDeathsCalc)    
    cDotArray.append(E/Tx)
    dDotArray.append(f*I/Ti)
    if theTime < tControl:  
      rhoI  = rhoI0; rhoD = rhoD0      
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

  return theTimes,cumCasesArray,cumDeathsArray,cDotArray,dDotArray

def main():

  k = 0.00787124323636
  tControl = 142.341834446
  Td = 1.43884846346
  rhoI0 = 1.17624112442
  rhoD0 = 0.084896642701
  c0 = 49.
  d0 = 6.
  Ti = 8.6  
  Tx = 9.   
  f = 0.316 
  tMax = 300.
  tS = 0.

  t,c,d,cd,dd = eirdModel(Tx,Ti,f,c0,d0,rhoI0,rhoD0,k,tControl,Td,tMax,tS)
  for i in range(0,len(t)):
    print t[i],c[i],d[i],cd[i],dd[i]
  
if __name__ == '__main__':
  main()
  
