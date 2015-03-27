from pymc import Uniform

# Data input and output file names
fileName      = "data/SL.dat"
outFolderName = "chainsSL"
output        = "SL1.mcmc"

# Number of samples, and burn-in period.
numSamples = 100000
numBurn    = 25000

# How many samples to be used for training.
trnLength = -1  # all samples.

# SL
Ti = 8.6     # Infection time.
Tx = 9.      # Incubation time.
f = 0.316    # Fatality rate 

# Liberia
#Ti = 7.9     # Infection time.
#Tx = 9.5     # Incubation time.
#f = 0.347    # Fatality rate 

# Guinea
#Ti = 6.4      # Infection time.
#Tx = 10.7     # Incubation time.
#f = 0.575     # Fatality rate 

# Markov Chain Montecarlo variables. Assuming uniform priors.
rhoI0     = Uniform('rhoI0',  0., 2., value=1.2)
rhoD0     = Uniform('rhoD0', 0., 2., value=1.2)
k         = Uniform('k', 0., 0.1, value=0.01)
tControl  = Uniform('tControl', 0., 300., value=200.)
Td        = Uniform('Td', 1., 6., value=3.)
