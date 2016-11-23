import time
import matplotlib.pyplot as plt

times, d = [], {}
for i in range(10000000):
  start = time.time()
  d[i] = i
  stop = time.time()
  times.append(stop-start)

plt.plot(times)
plt.xlabel("dictionary size")
plt.ylabel("time to add an element (seconds)")
plt.show()
