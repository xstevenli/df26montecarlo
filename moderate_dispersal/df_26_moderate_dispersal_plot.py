import pickle
import matplotlib.pylab as plt

df_26_baseline = pickle.load(open("df_26_moderate_dispersal.p", "rb"))

lists = sorted(df_26_baseline.items())

x, y = zip(*lists)

fig = plt.figure()
plt.plot(x, y)
fig.suptitle('20 DF-26s Striking 24 Open Parking Spots\nCEP = 50 m', fontsize=14)
plt.xticks(np.arrange(0,20,4))
plt.xlabel('Leaked DF-26 IRBMs', fontsize=14)
plt.ylabel('Aircraft Destroyed', fontsize=14)
plt.grid()
plt.show()

