import os
                
class Simpledb():
        def __init__(self, filename):
                self.filename = filename
        def __repr__(self):
                return ("<" + self.__class__.__name__ + ' file = ' + self.filename + '>')

        def addEntry(self, key, value):
                f = open(self.filename, 'a')
                f.write(key + '\t' + value + '\n')
                f.close() 
        def findEntry(self, key):
                f = open(self.filename, 'r')
                for row in f:
                       (k,v) = row.split('\t', 1)
                       if key in k:
                               return v[:-1]
                return None
                f.close()

        def deleteEntry(self, key):
                f = open(self.filename, 'r')
                result = open('result.txt', 'w')
                for row in f:
                        (k, v) = row.split('\t', 1)
                        if str(k) != str(key):
                                result.write(row)
                f.close()
                os.replace('result.txt', self.filename)

        def updateEntry(self, key, value):
                f = open(self.filename, 'r')
                result = open('result.txt', 'w')
                for row in f:
                        (k, v) = row.split('\t', 1)
                        if k == str(key):
                                result.write(str(key) + '\t' + str(value) + '\n')
                        else:
                                result.write(row)
                f.close()
                result.close()
                os.replace('result.txt', self.filename)




