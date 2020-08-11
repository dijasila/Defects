# create trees based on the database of initial host materials
asr run "database.totree materials.db -c 3 --atomsname unrelaxed.json --run"
mv tree0/ tree-sajid
mv tree1/ tree-simone
mv tree2/ tree-fabian
# go into the respective trees, then do 'mq init' and grant write permissions
# to the newly created .myqueue folder. Afterwards, set up the defect structures:
mq submit "asr.setup.defects --general_algorithm 15."
