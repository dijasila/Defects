# this is a simple script to collect all of the host supercells in a single database
# used in order to check whether the setup of supercells is fine for all of our systems
from ase.db import connect
from ase.io import read

db = connect('/home/niflheim2/cmr/WIP/defects/databases/host_sc.db')

sstruc = read('structure.json')
# pstruc = read('../unrelaxed.json')
# sc = sstruc.get_cell()
# pc = pstruc.get_cell()

db.write(sstruc)
