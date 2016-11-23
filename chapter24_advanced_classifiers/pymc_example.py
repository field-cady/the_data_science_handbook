import pymc
import mymodel
import matplotlib.pyplot as plt
S = pymc.MCMC(mymodel)
S.sample(iter = 40000, burn = 30000)
pymc.Matplot.plot(S)
plt.show()
