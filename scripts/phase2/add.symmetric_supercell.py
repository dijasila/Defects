##############################################################################
#============================================================================#
############################# !WORK IN PROGRESS! #############################
#============================================================================#
##############################################################################
# This script takes a relaxed defect structure (or pristine supercell) as
# input and maps the structure into a supercell that is simply a integer
# repetition of primitive unit cell of the material.
#
# It is needed for the analysis of local defect symmetries.

# TODO: implement check of number of atoms

from ase import Atoms
from ase.geometry import wrap_positions
from ase.io import read
from ase.visualize import view
from pathlib import Path
import numpy as np

p = Path('/home/niflheim2/cmr/WIP/defects/')
defectpaths = list(p.glob('tree-fabian/AB/129/**/defects.Br2Cs2_000.Br_Cs/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB2/187/SrCl2-AB2-187-b-i-0/defects.SrCl2_000.v_Cl/charge_0/'))
N_tot = len(defectpaths)
print('INFO: total number of defect systems: {}'.format(N_tot))

i = 0
for defect in defectpaths:
    if Path(str(defect.absolute()) + '/structure.json').is_file():
        print('INFO: reconstruct symmetric supercell!')
        #structure = read(Path(str(defect.absolute()) + '/structure.json'))
        structure = read(Path(str(defect.absolute()) + '/unrelaxed.json'))
        primitive = read(Path(str(defect.absolute()) + '/../../unrelaxed.json'))
        pristine = read(Path(str(defect.absolute()) + '/../../defects.pristine_sc/structure.json'))
        defecttype = str(defect.absolute()).split('/')[-2].split('_')[-2].split('.')[-1]
        # first, figure out how many repetitions are needed
        N = len(pristine)/len(primitive)
        n = int(np.floor(np.sqrt(N)))
        print(N, n)
        # second, set up new cell and put relaxed atoms into it
        reference = primitive.copy()
        reference = reference.repeat((n, n, 1))
        cell = reference.get_cell()
        if cell[1][1] > pristine.get_cell()[1][1]:
            n = n - 1
            reference = primitive.copy().repeat((n, n, 1))
            cell = reference.get_cell()
        positions = structure.get_positions()
        kinds = structure.get_chemical_symbols()
        ref_struc = Atoms(symbols=kinds, positions=positions, cell=cell)
        # third, remove atoms that do not fit into the symmetric SC anymore
        view(ref_struc)
        atomslist = []
        for i, element in enumerate(ref_struc):
            #if ((element.position[1] < ref_struc.get_cell()[1][1] and
            #        element.position[0] < 2*ref_struc.get_cell()[0][0])
            #        or i < len(primitive)):
            #if ((element.position[1] < ref_struc.get_cell()[1][1] and
            #        element.position[0] < 1*ref_struc.get_cell()[0][0])
            #        or i < len(primitive)):
            #if (element.position[1] < ref_struc.get_cell()[1][1] and
            #        element.position[0] < 1*ref_struc.get_cell()[0][0]):
            if i < len(primitive):
                print(element)
                atomslist.append(element)
            i += 1
        ref_struc = Atoms(symbols=atomslist, cell=cell)
        # finally, wrap atoms inside the cell and save the structure
        positions_new = wrap_positions(ref_struc.get_positions(),
                ref_struc.get_cell(), pbc=[1, 1, 0])
        ref_struc.set_positions(positions_new)
        print(structure, primitive, pristine)
        i += 1
        # check if number of atoms in the unit cell is correct
        if defecttype == 'v' and len(ref_struc) != (n * n * len(primitive) - 1):
            print('ERROR: number of atoms wrong in {}'.format(defect.absolute()))
        elif len(ref_struc) != (n * n * len(primitive)):
            print('ERROR: number of atoms wrong in {}'.format(defect.absolute()))
        else:
            print('INFO: number of atoms correct in {}'.format(defect.absolute()))
#view(structure)
#view(primitive)
view(ref_struc)

print(N_tot, i, float(N_tot)/i)
