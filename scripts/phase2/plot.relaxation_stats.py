# This routine goes through all of the defect folders in which a relaxation
# was conducted and analyses how many relaxation steps were needed to
# end up at the final structure

from pathlib import Path
from ase.io import Trajectory
import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored

p = Path('/home/niflheim2/cmr/WIP/defects/')
plotpath = '/home/niflheim2/cmr/WIP/defects/plots/phase2/'


# Width and height in pixels
ppi = 100
figw = 1200
figh = 700

# Visualize relaxation behaviour
fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)
plt.xlim(0,150)
plt.ylim(0,10)
#plt.xscale('log')
plt.xlabel('Number of relaxation steps', fontsize=14)
plt.ylabel('Energy difference in eV', fontsize=14)

# extract paths
treepaths = list(p.glob('tree-*'))
# initialize list for step histogram
count = []
n = 0
N = len(list(p.glob('tree-*/A*/**/**/**/**/charge_0/')))
for tree in treepaths:
    defectpaths = list(tree.glob('A*/**/**/**/**/charge_0/relax.traj'))
    for defect in defectpaths:
        energies = []
        steps = []
        parent = defect.parent
        traj = Trajectory(defect)
        # collect data for analysing the number of steps needed to fully relax
        if Path(str(parent.absolute()) + '/results-asr.relax.json').is_file():
            count.append(len(traj))
            print('INFO: relaxation of {} appended!'.format(parent.absolute()))
            for i in range(len(traj)):
                energies.append(traj[i].get_potential_energy() - traj[-1].get_potential_energy())
                steps.append(i)
            plt.plot(steps, energies, color='grey')
        else:
            print('INFO: relaxation in {} not finished!'.format(parent.absolute()))
            for i in range(len(traj)):
                energies.append(traj[i].get_potential_energy() - traj[-1].get_potential_energy())
                steps.append(i)
            plt.plot(steps, energies, color='red')
        if len(traj) > 200:
            print(colored('WARNING: system {} relaxed, but needed {} steps!'.format(
                parent.absolute(), len(traj)), 'red'))
        n += 1

plt.savefig(plotpath + 'relaxation_overview.png')

# visualize histogram of finished calculations
# Create histogram for number of atoms
fig = plt.figure(figsize=(figw / ppi, figh / ppi), dpi=ppi)

mean = np.mean(count)
relaxed = len(count)
print('INFO: successfully relaxed structures (of submitted calculations): {} of {} ({} %)'.format(
      relaxed, n, int(100*relaxed/float(n))))
print('INFO: successfully relaxed structures (total): {} of {} ({} %)'.format(
      relaxed, N, int(100*relaxed/float(N))))

plt.hist(count, 20, facecolor='grey', alpha=0.5)
plt.axvline(mean, color='red')
plt.xlabel('Number of relaxation steps', fontsize=14)
plt.savefig(plotpath + 'relaxation_histogram.png')
