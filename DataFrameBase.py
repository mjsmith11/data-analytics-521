from abc import ABCMeta, abstractmethod
from pandas import Series,DataFrame
import pandas as pd
import numpy as np
from datetime import datetime
import utilities as u

class DataFrameBaseType:
    'common base class for data in a dataframe'
    __metaclass__ = ABCMeta

    def __init__(self):
        self.empty = 1
        self.filepath = ""
        self.missingValues = 0
        self.df = None


    @abstractmethod
    def parseLine(self,line):
        pass


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
    """Adds a column named newColName with the day of the week calculated using data in the passed month, day, and year fields."""
    def addDayOfWeek(self,basedOnName,newColName):
        self.df[newColName] = self.df[basedOnName].map(lambda x: u.getDayOfWeek(x))


    def frequencies(self,field):
        return self.df[field].value_counts()


