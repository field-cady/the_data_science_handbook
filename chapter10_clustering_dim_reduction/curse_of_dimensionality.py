import numpy, scipy
d = 500
data = numpy.random.uniform(
    size=d*1000).reshape((1000,d))
distances = scipy.spatial.distance.cdist(data, data)
pd.Series(distances.reshape(1000000)).hist(bins=50)
plt.title("Dist. between points in R%i" % d)
plt.show()
