# this script is plotting all of the host supercells that are used to 
# incorporate defects in a pdf file for an overview
import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
from ase.db import connect
import numpy as np

db = connect('/home/niflheim2/cmr/WIP/defects/databases/host_sc.db')
N = db.count()
ncol = 1
fig, axes = plt.subplots(N, ncol, figsize=(10, ncol*N))
n = 0
for row in db.select():
    print(n, row.formula)
    plot_atoms(row.toatoms(), axes.flatten()[n], rotation=('0x,0y,0z'))
    axes.flatten()[n].set_title(row.formula)
    axes.flatten()[n].set_axis_off()
    n += ncol

plt.savefig('/home/niflheim2/cmr/WIP/defects/plots/phase1/structures_host.pdf')
