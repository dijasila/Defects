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


def get_supercell_shape(primitive, pristine):
    """
    Calculates which (NxNx1) supercell would be closest to the given supercell
    created by the general algorithm with respect to number of atoms.

    Returns: N
    """
    N = len(pristine)/len(primitive)
    return int(np.floor(np.sqrt(N)))


def recreate_symmetric_cell(structure, primitive, pristine):
    """
    Function that analyses supercell created by the general algorithm and
    creates symmetric supercell with the atomic positions of the general
    supercell.

    Note: The atoms are not correctly mapped in yet, and also the number
    of atoms is not correct here. It is done in the mapping functions.
    """
    reference = primitive.copy()
    N = get_supercell_shape(primitive, pristine)
    reference = reference.repeat((N, N, 1))
    cell = reference.get_cell()
    if cell[1][1] > pristine.get_cell()[1][1]:
        N = N - 1
        reference = primitive.copy()
        reference = reference.repeat((N, N, 1))
        cell = reference.get_cell()
    bigatoms = structure.repeat((5,5,1))
    positions = bigatoms.get_positions()
    positions += np.array([-3*cell[0][0], -2*(cell[0][1] + cell[1][1]), 0])
    kinds = bigatoms.get_chemical_symbols()
    ref_struc = Atoms(symbols=kinds, positions=positions, cell=cell)

    return ref_struc, cell, N


def is_vacancy(defectpath):
    """
    Checks whether the current defect is a vacancy or substitutional defect.
    Returns true if it is a vacancy, false if it is a substitutional defect.
    """
    defecttype = str(defectpath.absolute()).split(
            '/')[-2].split('_')[-2].split('.')[-1]
    if defecttype == 'v':
        return True
    else:
        return False


def conserved_atoms(ref_struc, primitive, N, defectpath):
    """
    Returns True if number of atoms is correct after the mapping,
    False if the number is not conserved.
    """
    if (is_vacancy(defectpath) and len(ref_struc) != (N * N * len(primitive) - 1)):
        print('ERROR: number of atoms wrong in {}'.format(
            defectpath.absolute()))
        return False
    elif (not is_vacancy(defectpath) and len(ref_struc) != (N * N * len(primitive))):
        print('ERROR: number of atoms wrong in {}'.format(
            defectpath.absolute()))
        return False
    else:
        print('INFO: number of atoms correct in {}'.format(
            defectpath.absolute()))
        return True


def remove_atoms(structure, indexlist):
    indices = np.array(indexlist)
    print(indices)
    indices = np.sort(indices)[::-1]
    print(indices)
    for element in indices:
        structure.pop(element)
    return structure


def indexlist_cut_atoms(structure):
    cell = structure.get_cell()
    indexlist = []
    for i in range(len(structure)):
        pos = structure.get_scaled_positions()[i]
        # save indices that are outside the new cell
        if abs(max(pos) > 0.99) or min(pos) < -0.01:
            indexlist.append(i)

    return indexlist



p = Path('/home/niflheim2/cmr/WIP/defects/')
#defectpaths = list(p.glob('tree-fabian/AB/129/**/defects.Br2Cs2_000.*_Cs/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB2/187/SrCl2-AB2-187-b-i-0/defects.SrCl2_000.v_Cl/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB/129/**/Br*v_Cs/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB2/187/SrCl2-AB2-187-b-i-0/defects.SrCl2_000.v_Sr/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB2/**/**/defects.*/charge_0/'))
#defectpaths = list(p.glob('tree-fabian/AB2/115/ZnI2-AB2-115-d-g-0/defects.ZnI2_000.v_Zn/charge_0'))
#defectpaths = list(p.glob('tree-simone/AB2/187/MoS2-AB2-187-b-i-0/defects.MoS2_000.v_S/charge_0'))
defectpaths = list(p.glob('tree-*/A*/**/**/**/charge_0/'))
N_tot = len(defectpaths)
print('INFO: total number of defect systems: {}'.format(N_tot))

i = 0
j = 0
for defect in defectpaths:
    if Path(str(defect.absolute()) + '/structure.json').is_file():
        print('INFO: reconstruct symmetric supercell!')
        #structure = read(Path(str(defect.absolute()) + '/structure.json'))
        structure = read(Path(str(defect.absolute()) + '/unrelaxed.json'))
        primitive = read(Path(str(defect.absolute()) + '/../../unrelaxed.json'))
        pristine = read(Path(str(defect.absolute()) + '/../../defects.pristine_sc/structure.json'))
        ref_struc, cell, N = recreate_symmetric_cell(structure, primitive, pristine)
        #view(ref_struc)
        indexlist = indexlist_cut_atoms(ref_struc)
        ref_struc = remove_atoms(ref_struc, indexlist)
        #view(ref_struc)
        if is_vacancy(defect):
            print('INFO: vacancy defect!')
            N_prim = len(primitive) - 1
        else:
            print('INFO: substitutional defect!')
            N_prim = len(primitive)
        if conserved_atoms(ref_struc, primitive, N, defect):
            i += 1
        j += 1
        #view(structure)
print('Systems with conserved atom number: {} of {}.'.format(
    i, j))

