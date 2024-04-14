import matplotlib.pyplot as plt

with open('data.txt') as f:
    lines = f.readlines()
    distance = [float(line.split()[0]) for line in lines]
    voltage = [float(line.split()[1]) for line in lines]

plt.xlabel('distance')
plt.ylabel('voltage')
plt.plot(distance, voltage)
plt.show()
