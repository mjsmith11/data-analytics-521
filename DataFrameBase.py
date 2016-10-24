#Matthew Smith
#CS521 Project 3
#Base Class for analysis with a DataFrame

from abc import ABCMeta, abstractmethod
from pandas import DataFrame
import utilities as u

class DataFrameBaseType:
    'common base class for data in a dataframe'
    __metaclass__ = ABCMeta

    #this should be invoked by derived class constructor
    def __init__(self):
        self.empty = 1
        self.filepath = ""
        self.missingValues = 0
        self.df = None

#to be implemented in derived classes for parsing a line of a raw file and returning a python list of values. It may return
#-1 to omit a record in an incorrect format
    @abstractmethod
    def parseLine(self,line):
        pass

#uses the parseLine method implemented in derived classes to create a dataframe as a member of the class of the data at the path provided as a parameter.
#This relies on self.columnNames to be defined as a python list in the derived class constructor
    def readSingleLineRecordsSemiStructured(self,filepath):
        self.filepath = filepath
        self.missingValues = 0

        f = open(filepath)
        data = []
        for line in f:
            result = self.parseLine(line)
            if result == -1:
                self.missingValues += 1
            else:
                data.append(result)
        f.close()

        if len(data)!=0:
            self.empty = 0
            self.df = DataFrame(data,columns=self.columnNames)

    #Adds a column named newColName with the day of the week calculated using data in the passed basedOnName field Example date 9/Nov/2013.
    def addDayOfWeek(self,basedOnName,newColName):
        self.df[newColName] = self.df[basedOnName].map(lambda x: u.getDayOfWeek(x))

    #returns a series with the frequencies of values in the passed field
    def frequencies(self,field):
        return self.df[field].value_counts()

    #returns a series with the n(parameter) most frequent values for the passed field that match the passed regular expression.
    # the series indices are the data values and the series values represent the frequency of its index
    def filteredTopNFreq(self,regex,n,field):
        frequencies = self.frequencies(field)
        filtered = frequencies.filter(regex=regex)
        if (filtered.size<=n):
            return filtered
        else:
            return filtered[:n]
