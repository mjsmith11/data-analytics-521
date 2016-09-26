import matplotlib.pyplot as plot

#creates and shows a pie chart with shadow and largest slice exploded
#parameters
#   data: A dictionary of the data to be displayed. Pie slices are labeled with the keys and percentages. Values determine the size of the slices
#   minPercent: data keys with a lower percentage of the whole than this parameter are grouped and displayed under 'Other Values'
#   title: displayed at the top of the chart
def piechart(datadict, minPercent, title):
    labels = []
    values = []
    for key in datadict.keys():
        if key != "" and datadict[key] != 0:
            labels.append(key)
            values.append(datadict[key])

    sumvals = sum(values)

    #remove values less that the threshold and agregate them into an other values category
    otherThres = sumvals*minPercent/100.
    otherTotal = 0
    indicesToDelete = []
    for i,val in enumerate(values):
        if(val < otherThres):
            otherTotal = otherTotal + val
            indicesToDelete.append(i)

    indicesToDelete.sort()
    indicesToDelete.reverse()
    for i in indicesToDelete:
        del values[i]
        del labels[i]

    if(otherTotal>0):
        labels.append("Other Values")
        values.append(otherTotal)

    maxval = max(values)
    explode =[]
    for val in values:
        if val == maxval:
            explode.append(0.1)
        else:
            explode.append(0)

    plot.pie(values,labels=labels,autopct='%1.1f%%',explode = explode,shadow=True)
    plot.title(title)
    plot.show()

def positiveLogHistogram(dataarr,title,xlabel):
    poslist = []
    for val in dataarr:
        if val >= 0:
            poslist.append(val)
    plot.hist(poslist,bins=20,log=True)
    plot.grid(True)
    plot.xlabel(xlabel)
    plot.ylabel("log(Frequency)")
    plot.title(title)
    plot.show()

#creates and shows a scatter plot with teh provided data and labels
#data should be in a dictonary with index 'x' being a list of x values and 'y' being a list of 'y' values
def scatter(data,xlabel,ylabel,title):
    plot.scatter(data['x'],data['y'])
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)
    plot.title(title)
    plot.axis("equal")
    plot.show()