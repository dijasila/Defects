# This routine analyses the calculations that did not relax and
# showed a convergence error.

# TODO: magnetic moments
# TODO: more criteria

from pathlib import Path
from ase.io import Trajectory

p = Path('/home/niflheim2/cmr/WIP/defects/')
failedpaths = list(p.glob('tree-*/A*/**/**/**/**/charge_0/asr.relax*.FAILED'))

i = 0
N = len(failedpaths)
for failed in failedpaths:
    print('INFO: failed relaxation in {}'.format(failed.parent.absolute()))
    traj = Trajectory(str(failed.parent.absolute()) + '/relax.traj')
    try:
        lastatom = traj[-1]
        if abs(lastatom.get_magnetic_moment()) > 0.001:
            print('INFO: magnetic moment present!')
            i += 1
    except IndexError:
        print('WARNING: no relaxation step conducted!')

print('=======================================================')
print('====================== SUMMARY ========================')
print('=======================================================')
print('INFO: {} of {} failed relaxations are magnetic! '
      '({} %)'.format(i, N, int(i*100./N)))
