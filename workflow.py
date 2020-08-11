"""Workflow for HT defect project."""
from myqueue.task import task
from pathlib import Path
from asr.core import read_json
import sys
import myqueue as mq
from termcolor import colored

# check whether the correct version of MyQueue is present
current_version = '20.5.0'
if mq.__version__ == current_version:
    print(colored('INFO: using correct version of MyQueue ({}). Proceed setting '
          'up tasks.'.format(mq.__version__), 'green'))
else:
    print(colored('ERROR: wrong version of MyQueue ({}) is used. Did you activate the '
          'correct virtual environment (with version {})?'.format(
              mq.__version__, current_version), 'red'))
    sys.exit()

def create_tasks():
    """Generate all tasks for myqueue for a specific material."""
    tasks = []

    def append(*args, **kwargs):
        """Append a task."""
        assert "creates" in kwargs
        tasks.append(task(*args, **kwargs))

    folder = Path().absolute()
    # submit relaxations and gs calculations of the defect systems
    if (obtain_system_size() < 0.7e7 and
            (folder.name.startswith('charge')
             or folder.name.startswith('defects.pristine_sc'))):
        if folder.name.startswith('charge'):
            print('INFO: add tasks for this material to the workflow!')
            append('asr.relax --fixcell --allow-symmetry-breaking '
                   '--dont-enforce-symmetry',
                   resources='40:2d', restart=2,
                   creates=['results-asr.relax.json'])
            append("asr.structureinfo", resources="1:10m",
                   creates=['results-asr.structureinfo.json'],
                   deps="asr.relax+--fixcell_--allow-symmetry-breaking"
                   "_--dont-enforce-symmetry")
            append('asr.gs@calculate', resources='40:1d',
                   creates=['results-asr.gs@calculate.json'],
                   deps='asr.relax+--fixcell_--allow-symmetry-breaking'
                   '_--dont-enforce-symmetry')
            append('asr.gs', resources='24:xeon24_512:1h',
                   creates=['results-asr.gs.json'],
                   deps='asr.gs@calculate')
        elif (folder.name.startswith('defects.pristine_sc')):
            print('INFO: add pristine calculations to the workflow!')
            append('asr.gs@calculate', resources='40:1d',
                   creates=['results-asr.gs@calculate.json'])
            append('asr.gs', resources='40:2h',
                   creates=['results-asr.gs.json'],
                   deps='asr.gs@calculate')
    elif not (folder.name.startswith('charge') or
              folder.name.startswith('defects.pristine_sc')):
        print('WARNING: please submit the workflow to either the pristine'
              f' or charge state folders of the defect!')
    else:
        print('INFO: skip large material!')

    # # once initial relaxations and gs calculations are done, start with
    # # SJ part of the workflow. First, set up the folders.
    # if folder.name.startswith('charge'):
    #     print('INFO: create folders for SJ calculations!')
    #     append('asr.setup.defects --halfinteger True',
    #            resources='1:10m',
    #            creates=['results-asr.setup.defects.json'],
    #            deps=['asr.gs'])
    # # second, submit the gs calculations within the half integer folders
    # if (folder.name.startswith('sj') and
    #         Path('params.json').is_file() and
    #         Path('structure.json').is_file() and
    #         Path('results-asr.gs.json').is_file()):
    #     append('asr.gs@calculate', resources='40:1d',
    #            creates=['results-asr.gs@calculate.json'],
    #            deps=['../asr.gs'])
    #     append('asr.gs', resources='40:2h',
    #            creates=['results-asr.gs.json'],
    #            deps='asr.gs@calculate')
    #     print('INFO: submit SJ calculations!')

    return tasks


def obtain_system_size():
    """Reads in the structure and calculates the product of cell volume times
    number of electrons."""
    from ase.io import read

    folder = Path().absolute()
    # read in the unrelaxed structure
    if folder.name.startswith('defects.pristine_sc'):
        atoms = read('structure.json')
    else:
        atoms = read('unrelaxed.json')

    el = 0
    for i in range(len(atoms)):
        el += atoms.get_atomic_numbers()[i]

    return el*atoms.get_volume()
