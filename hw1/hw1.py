import csv
import matplotlib.pyplot as plt
import numpy as np

data = open("downloads.txt", "r")
reader = csv.reader(data, delimiter=",")
x = []
y = []
sumx = 0
sumy = 0
sumxy = 0
sumx2 = 0
sumy2 = 0
count = 0

for row in reader:
	if row[1] != 'nan':
		tx = float(row[0])
		ty = float(row[1])
		sumx += tx
		sumy += ty
		sumxy += tx*ty
		sumx2 += tx*tx
		sumy2 += ty*ty
		count += 1
		x.append(tx)
		y.append(ty)

x = np.asarray(x)
y = np.asarray(y)
m = ((count*sumxy) - (sumx*sumy)) / ((count*sumx2) - (sumx*sumx))
b = (sumy - (m*sumx)) / count

plt.scatter(x, y)
plt.plot(x, m*x + b, '-', linewidth=2.0, color="r")

plt.xlabel('Time')
plt.ylabel('Downloads')
plt.title('Scatter Plot of Downloads vs Time')
plt.axis([0, 750, 0, 6000])
plt.show()