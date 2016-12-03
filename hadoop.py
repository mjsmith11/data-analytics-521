from datetime import datetime
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cPickle as pickle

class TopN(object):
    def __init__(self,size):
        self.size = size
        self.currentSize = 0
        self.min = 0
        #self.max = 0
        self.head = None

    def insert(self,data):
        new_node = Node(data)
        if(self.head == None):
            new_node.set_next(None)
            self.head = new_node
            self.currentSize += 1
            self.min = data[1]
        elif(data[1]>self.min or self.currentSize<self.size):
            #keep the list sorted because we have to delete the smallest to keep to size
            current = self.head
            while(current.get_next() != None and current.get_next().get_data()[1] < new_node.get_data()[1]):
                current = current.get_next()
            new_node.set_next(current.get_next())
            current.set_next(new_node)
            if(self.currentSize<self.size):
                self.currentSize += 1
            else:
                self.head = self.head.get_next() ; #maintain the size drop the smallest
            self.min = self.head.get_data()[1]

    def printToStdOut(self):
        current = self.head
        while(current.get_next() != None):
            print current.get_data()
            current = current.get_next()
    def getdict(self):
        result = {}
        current = self.head
        while (current.get_next() != None):
            result[current.get_data()[0]] = current.get_data()[1]
            current = current.get_next()
        return result
    def getTuples(self):
        result = []
        current = self.head
        while (current.get_next() != None):
            result.append((current.get_data()[0],current.get_data()[1]))
            current = current.get_next()
        return result


class Node(object):
    def __init__(self,data=None,next_node=None):
        self.data = data
        self.next_node = next_node


    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self,new_next):
        self.next_node = new_next

print datetime.now().time()
stub = ""
totalWords = 0
totalDistinct = 0
top = TopN(500)
for fnum in range(42):
    filepath = stub+"part-000"
    if(fnum<10):
        filepath = filepath + "0"
    filepath = filepath+str(fnum)

    print filepath
    f = open(filepath)
    for line in f:
        splits =  line.split('\t')
        splits[1] = int(splits[1])
        totalWords += splits[1]
        totalDistinct += 1
        if splits[0].isalpha():
            top.insert(splits)
    f.close()

print totalWords
print totalDistinct

stopwords = set(STOPWORDS)
tuples = top.getTuples()
try:
    pickle.dump(tuples, open("C:\\io\\hadooptuples.p", "wb"))
except:
    print "pickle pooped"
print tuples[400:]
wordcloud = WordCloud(max_font_size=40,stopwords=stopwords).generate_from_frequencies(tuples)

plt.imshow(wordcloud)
plt.axis("off")
#plt.figure()
print datetime.now().time()
plt.show()