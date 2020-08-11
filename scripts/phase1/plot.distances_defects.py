# analyses the supercell host structures to give an overview on the distriburion
# of nearest defect, next nearest defect, and so on is throughout the set of
# materials
import matplotlib.pyplot as plt
from ase.db import connect
import numpy as np

db = connect('/home/niflheim2/cmr/WIP/defects/databases/host_sc.db')
nearest1 = []
nearest2 = []
nearest3 = []
for i, row in enumerate(db.select()):
    cell = row.toatoms().get_cell()
    # compute distances between mirroring defects
    distances = []
    distance_xx = np.sqrt(cell[0][0]**2 + cell[0][1]**2 + cell[0][2]**2)
    distance_yy = np.sqrt(cell[1][0]**2 + cell[1][1]**2 + cell[1][2]**2)
    distance_xy = np.sqrt((
        cell[0][0] + cell[1][0])**2 + (
        cell[0][1] + cell[1][1])**2 + (
        cell[0][2] + cell[1][2])**2)
    distance_mxy = np.sqrt((
        -cell[0][0] + cell[1][0])**2 + (
        -cell[0][1] + cell[1][1])**2 + (
        -cell[0][2] + cell[1][2])**2)
    distances = np.array([distance_xx, distance_yy, distance_xy, distance_mxy])
    # evaluate nearest neighboring defect
    nearest1.append(min(distances))
    # continue analysis for defects further away
    nearest2.append(np.partition(distances, 1)[1])
    nearest3.append(np.partition(distances, 2)[2])

# Create histogram of the distances
# Width and height in pixels
ppi = 100
figw = 1200
figh = 700

fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

mean1 = np.mean(nearest1)
plt.hist(nearest1, 20, facecolor='grey', alpha=0.5)
plt.axvline(mean1, color='red')
plt.xlabel('Nearest distance to mirroring defect in $\AA$', fontsize=14)

plt.savefig('/home/niflheim2/cmr/WIP/defects/plots/phase1/histogram.distances_host_1.png')


fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

mean2 = np.mean(nearest2)
plt.hist(nearest2, 20, facecolor='grey', alpha=0.5)
plt.axvline(mean2, color='red')
plt.xlabel('Second nearest distance to mirroring defect in $\AA$', fontsize=14)

plt.savefig('/home/niflheim2/cmr/WIP/defects/plots/phase1/histogram.distances_host_2.png')


fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

mean3 = np.mean(nearest3)
plt.hist(nearest3, 20, facecolor='grey', alpha=0.5)
plt.axvline(mean3, color='red')
plt.xlabel('Third nearest distance to mirroring defect in $\AA$', fontsize=14)

plt.savefig('/home/niflheim2/cmr/WIP/defects/plots/phase1/histogram.distances_host_3.png')


fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

mean1 = np.mean(nearest1)
mean2 = np.mean(nearest2)
mean3 = np.mean(nearest3)
plt.hist(nearest1, 20, facecolor='grey', alpha=0.5)
plt.hist(nearest2, 20, facecolor='blue', alpha=0.3)
plt.hist(nearest3, 20, facecolor='orange', alpha=0.3)
plt.axvline(mean1, color='black')
plt.axvline(mean2, color='blue')
plt.axvline(mean3, color='orange')
plt.xlabel('Three nearest distances to mirroring defects in $\AA$', fontsize=14)

plt.savefig('/home/niflheim2/cmr/WIP/defects/plots/phase1/histogram.distances_host_all.png')
