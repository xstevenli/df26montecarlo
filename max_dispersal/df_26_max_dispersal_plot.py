import pickle
import matplotlib.pylab as plt

df_26_baseline = pickle.load(open("df_26_max_dispersal.p", "rb"))

lists = sorted(df_26_baseline.items())

x, y = zip(*lists)

fig = plt.figure()
plt.plot(x, y)
fig.suptitle('5 DF-26s Striking 6 Open Parking Spots\nCEP = 50 m', fontsize=14)
plt.xlim([0, 5])
plt.ylim([0, 6])
plt.xlabel('Leaked DF-26 IRBMs', fontsize=14)
plt.ylabel('Aircraft Destroyed', fontsize=14)
plt.grid()
plt.show()