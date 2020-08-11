# Welcome to the defect HT project

This introduction gives an overview of the structure of the defect HT project and
should be updated whenever new important information is coming up. It also describes
how we plan to do things in order to obtain consistent results and have a consistent
way of running calculations, extracting data, and visualizing results.

It is structured the following way:
    0. Folder structure
    1. General
    2. Submitting and running calculations
    3. How to deal with failed calculations
    4. How to extract data
    5. How to plot things
    6. Misc


0. Folder Structure
===================
Let's try to keep the folder structure as simple as possible. I have structured the
current version of our project in the following way (changes can be applied, I am
happy about good suggestions from you):

- Our projects directory is: /home/niflheim2/cmr/WIP/defects
- First, we have three trees, each of which one of us runs its respective calculations
  in. I.e. tree-sajid, tree-simone, tree-fabian. Within those folders we have the host
  materials, as well as all of our defect folders and materials. How the defect folders
  are structured is described in the docstring of asr.setup.defects.
- For each of those trees, I set up separate queues for MyQueue such that all the
  calculations we run are correctly tracked.
- Second, the folder 'venv/': in this folder, I set up the virtual environment with all
  of the packages we need (GPAW, ASE, ASR, MyQueue and more). In general, we should not
  change anything here, unless it is absolutely vital. If so, I would take care of the
  specifics here.
- Third, there are some important files in here. For example, 'workflow.py', 'materials.db',
  'get_materials.py'. I suggest that we aim to keep it to the essentials here. All of the
  special scripts, plots, databases and so on should be stored in the designated folders, as
  will be discussed in the next points.
- The 'databases/' folder: of course, we want to have our big final database in the end.
  On top of that it might also be necessary to do some pre-analysis and have several
  smaller databases to figure out things. We store all of those databases in here, and
  also make several backups in order to ensure we don't mess up something.
- The 'scripts/' and 'plots/' folders: the names speak for themselves here. All of the
  extraction, analysis, ... scripts should be in the first one of those, whereas all
  scripts that are connected to actually plotting data will be stored in the 'plots/'
  folder. Note, that withing those respective folders, I have created subfolders for the
  different phases of the project, see 1. chapter (general). Depending on which phase
  of the project your script/plotting routine focussed on, it needs to be stored in the
  respective folder.
- Naming convention for scripts and plotting routines:
    * All plotting scripts and extraction scripts are supposed to be stored in the
      'scripts/' folder and the respective subfolder 'phase{1,2,3,4}/'.
    * Naming convention: '{type}.{label}.py'.
    * 'type' specifies what kind of script you are dealing with. Possible types
      are: 'db' (a script that extracts some kind of database), 'plot' (plotting script),
      'analyse' (script to analyse outcomes of calculations like validity checks, error
      analysis, general analysis that doesn't end up in a database), 'add' (adding information
      or changing files for compability with analysis scripts), ...
    * 'label' should give a very short label on what is done within the script.
    * For example, a script that extracts a database containing information about the
      host systems without defects could be called 'db.hosts.py'.
    * Any other suggestions for naming conventions here?
- I created a file ('ISSUES.txt') where we should collect all of the things that need
  to be fixed or the ones that are not working at the moment. With this, we can keep
  track of all of the issues that need to be handled without forgetting them.


1. General
==========
- We want to always use the same versions of software. Therefore, I created a virtual
  environment, in which we should aim to run everything. Although MyQueue always detects
  the correct virtual environment while submitting jobs, I suggest we always activate
  the environment before we start working on the project. Therefore, all you need to do
  is: source '/home/niflheim2/cmr/WIP/defects/venv/activate'.
- I have set up MyQueue for us already and I think it is best if each one of us has
  his individual queue within his tree. Having said that, I ensured that all of us have
  the correct permission such that we can still submit jobs in each others trees. That
  might come in handy during the extraction phase of the project (phase2). Note: in
  general, let's still aim to restrict ourselves to run stuff in our own tree and
  only go into the other ones for specific purposes.
- As was seen in the 0. chapter (folder structure), I propose to split the project into
  three phases. They are:
    * Phase 1: Setting things up for the big project, analysis of different parts
               before the actual launch, setting up the workflow, and so on...
    * Phase 2: Running the workflow, analysing the progress during, conducting
               sanity checks, tracking the progress, possibly rescoping, ...
    * Phase 3: After the calculations ran, we focus on extracting data, analysing results,
               doing performance analysis, and so on.
    * Phase 4: Presenting the database


2. Submitting and Running Calculations
======================================
- In general, we aim to always submit the calculations using the workflow we have set up.
  You can find it in the main folder under 'workflow.py'. Within this workflow, I have
  added some easy checks whether you submitted it in the right folders, but always take
  care to submit it correctly. Also, keep in mind to always use the '-z' option of
  MyQueue first, in order to do the dry run. After that is done, you can submit the
  workflow for good. Note: the workflow in the main folder will probably be updated quite
  a lot of times and, therefore, it might be a good idea to copy it also to your
  respective tree. Note: submit a workflow always with 'mq workflow workflow.py folders/'.
- Sometimes, there might be tasks that you want to submit without the workflow. When doing
  that, please ensure to also submit it with MyQueue such that we can always keep track
  of what we actually ran and what we didn't.
- For calculations and analysis that is not part of the workflow or the general outline of
  the database, I would suggest that we always create individual folders (but not within
  the respective materials, in order to make sure we can easily extract things afterwards).
  Thus, I have created a 'misc/' folder within each of our trees that is dedicated to those
  kind of 'unplanned' calculations. When doing this, we will have a clear structure of our
  material tree.
- Within that 'misc/' folder, you can set up whichever folder structure you need or want.


3. How to Deal with Failed, Running, Finished Calculations
===========================================================
- Always try to avoid removing calculations with MyQueue. When calculations fail, run out
  of time, are cancelled, or else, try resubmitting them with improved parameters, settings,
  or similar in order to ensure we log all of our calculations with MyQueue correctly.
- When calculations fail, try to figure out what went wrong and depending on the outcome,
  resubmit the calculation.
- If possible, try to implement scripts that can analyse running, finished calculations and
  conduct simple validity checks in order to see whether a calculation makes sense. Those
  checks should be more thourough than the status of MyQueue, but also should not contain
  analysing the entire calculations. I guess discussing that at some point is the best idea.
- At some point we need to write scripts that give us an overview of the status of the
  calculations. (Just as a reminder to keep in mind.)


4. How to Extract Data
======================
- Aim to store everything in ASE database format. This can come in handy when plotting
  results at a later stage. Of course, for some cases that is not possible. Here, you
  can choose other methods to achieve your goal.
- One important point is that we discuss how we specifically store results in the big
  database. We should discuss it soon.
- Whenever we extract data, we should try to write general scripts that are applicable to
  run on the entire tree. Depending on the phase your script belongs to, save it in the
  corresponding folder as discussed in chapter 0 (folder structure).
- Before extracting the big database, it might be advantageous to also check different
  smaller parts or save subsets. When doing that, save the resulting databases in the
  'databases/' folder.


5. How to Plot Things
=====================
- Similar to the extraction part, always aim to develop general plotting scripts that
  are applicable to a all of our systems and that can be reused. If possible, plot
  things using the data that is saved in an ASE database.
- All plotting scripts are supposed to be saved in the 'scripts/' folder and the
  respective 'phase{1,2,3,4}/' folder depending on the stage of the project it belongs
  to. Always name plotting scripts in the following way: 'plot.{}.py' where you put
  a short label that let's others know what can be found in this script within the '{}'.


6. Misc
=======

