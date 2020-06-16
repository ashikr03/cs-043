from 3_1 import Simpledb
db = Simpledb('recipes.txt')
db.addEntry('relish', 'pickled cucumber and sugar')
print(db.findEntry("relish"))
