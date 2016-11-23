import pandas as pd
import sklearn.datasets as ds
import pymc

# Make Pandas dataframe
bs = ds.load_boston()
df = pd.DataFrame(bs.data, columns=bs.feature_names)
df['MEDV'] = bs.target

# Unknown parameters are A, B and C
A = pymc.Exponential('A', beta=1)
B = pymc.Exponential('B', beta=1)
C = pymc.Exponential('C', beta=1)
ptratio = pymc.Exponential(
  'ptratio', beta=df.PTRATIO.mean(),
  observed=True, value=df.PTRATIO)
crim = pymc.Exponential('crim',
  beta=A*ptratio, observed=True, value=df.CRIM)
rm = pymc.Normal('rm', mu=df.RM.mean(), 
  tau=1/(df.RM.std()**2), value=df.RM, observed=True)
medv = pymc.Normal('medv', mu=B*rm*(C-crim), 
  value=df.MEDV, observed=True)
