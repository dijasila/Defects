from ase.db import connect

# use C2DB in order to extract all of the materials that match our designated criteria
c2db = connect('c2db.db')
# write new database with our full set of host materials
materials = connect('materials.db')
#for i, row in enumerate(c2db.select('gap>=1',is_magnetic=False,dynamic_stability_level=3,thermodynamic_stability_level=3)): #,first_class_materials=True)):
for i, row in enumerate(c2db.select('gap>=1',is_magnetic=False,
    first_class_material=True,thermodynamic_stability_level=3,
    dynamic_stability_phonons='high',dynamic_stability_stiffness='high')):
    print(i, row.formula)
    materials.write(row.toatoms())

print('Wrote full set of host materials to materials.db!')
