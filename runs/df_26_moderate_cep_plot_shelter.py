import pickle
import matplotlib.pylab as plt

cep_50 = pickle.load(open("df_26_moderate_dispersal_shelter.p", "rb"))
cep_100 = pickle.load(open("df_26_moderate_dispersal_shelter_cep_100.p", "rb"))
cep_300 = pickle.load(open("df_26_moderate_dispersal_shelter_cep_300.p", "rb"))

cep_50_list = sorted(cep_50.items())
cep_100_list = sorted(cep_100.items())
cep_300_list = sorted(cep_300.items())

q, r = zip(*cep_50_list)
x, y = zip(*cep_100_list)
s, t = zip(*cep_300_list)

fig = plt.figure()

plt.plot(q, r, '-r', label='CEP = 50 m')
plt.plot(x, y, '-b', label='CEP = 100 m')
plt.plot(s, t, '-g', label='CEP = 300 m')

plt.legend(loc='upper left')
fig.suptitle('20 DF-26s Striking 24 RDS Parking Spots\nVaried CEP Levels', fontsize=14)
plt.xlabel('Leaked DF-26 IRBMs', fontsize=14)
plt.ylabel('Aircraft Destroyed', fontsize=14)
plt.grid()
plt.show()