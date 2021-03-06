#Matthew Smith
#CS521 Project 2
#frequency for string data and basic analytics for numerical data

import utilities as u
import numpy as np
import cPickle as pickle


# accepts a list of pickle files created by ingestion.py and field name as a string
# returns a dictionary with data values from the provided field in the provided data as keys and number of occurances as values
def frequencies(dataPickles, field):
    result = {}
    for file in dataPickles:
        data = pickle.load(open(file, "rb"))
        for row in data:
            value = row[u.indexLookup(field)]
            if (result.has_key(value)):
                result[value] = result[value] + 1
            else:
                result[value] = 1

    return result


# accepts a list of pickle files created by ingestion.py and field name as a string
# returns a dictionary with 2 entries. The numpy array with key 'array' and the number of missing elements with key 'missing elements'
def getNumpyArray(dataPickles, field):
    mylist = []
    missingElements = 0
    fieldNum = u.indexLookup(field)

    for file in dataPickles:
        data = pickle.load(open(file,"rb"))
        for row in data:
            if row[fieldNum] == "":
                missingElements += 1
            else:
                mylist.append(row[fieldNum])

    return {'array':np.array(mylist), 'missing elements':missingElements}

#accepts an array of numbers as a parameter
#returns an dictionary with element 'array' containing the array with outliers removed and element 'outliers' containing a list of removed values
#values that are not within 3 standard deviations of the mean are considered outliers
def removeOutliers(array):
    mean = np.mean(array)
    stddev = np.std(array)
    upperbound = mean+3*stddev
    lowerbound = mean-3*stddev
    removeIndices = []
    removedValues = []
    for i,num in enumerate(array):
        if num>upperbound or num<lowerbound:
            removeIndices.append(i)
            removedValues.append(num)
    array = np.delete(array,removeIndices)
    return {'array':array,'outliers':removedValues}

#returns a dictionary with the following analytics computed for the passed array
#   'n'                 : number of data values including outliers
#   'number of outliers : number of outliers that were removed
#   'outliers'          : a list of outliers that were removed
#   'max'               : max of the data excluding outliers
#   'min'               : min of the data excluding outliers
#   'mean'              : mean of the data excluding outliers
#   'median'            : median of the data excluding outliers
#   'Q1'                : the first quartile of the data excluding outliers
#   'Q3'                : the third quartile of the data excluding outliers
#   'stddev'            : standard deviation of the data excluding outliers
def computeBasicNumericalAnalytics(array):
    result = {}
    result['n'] = len(array)
    outlierDict = removeOutliers(array)
    noOutlierArr = outlierDict['array']
    result["number of outliers"] = len(outlierDict['outliers'])
    result['outliers'] = outlierDict['outliers']
    result['max'] = np.amax(noOutlierArr)
    result['min'] = np.amin(noOutlierArr)
    result['mean'] = np.mean(noOutlierArr)
    result['median'] = np.median(noOutlierArr)
    result['Q1'] = np.percentile(noOutlierArr,25)
    result['Q3'] = np.percentile(noOutlierArr,75)
    result['stddev'] = np.std(noOutlierArr)

    return result

#returns a dictionary representing ordered pairs from the xfield and yfield supplied. Key 'x' is a list of x values. key 'y' is a list of y values
#data objects missing either of these fields are not included
#data with either field exceeding the specified max are not included.

def getOrderedPairs(xfield,yfield,dataPickles,max):
        xlist = []
        ylist = []
        xfieldnum = u.indexLookup(xfield)
        yfieldnum = u.indexLookup(yfield)
        for file in dataPickles:
            data = pickle.load(open(file, "rb"))
            for row in data:
                if(row[xfieldnum]!="" and row[yfieldnum]!="" and row[xfieldnum]<max and row[yfieldnum]<max):
                    xlist.append(row[xfieldnum])
                    ylist.append(row[yfieldnum])

        return {'x':xlist,'y':ylist}