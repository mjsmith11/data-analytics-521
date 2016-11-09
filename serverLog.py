#Matthew Smith
#CS521 Project 3
#Class Derived from DataFrameBase for analyzing NASA web server log

# coding=utf-8

import re
import utilities as u
from pandas import DataFrame
from DataFrameBase import DataFrameBaseType
import matplotlib.pyplot as plot


class serverLog(DataFrameBaseType):
    def __init__(self):
        self.columnNames = ['requester','date','month','day','year','time','hour','minute','second','tz','verb','resource','protocol','response','size']
        self.sessiondf = None
        super(serverLog,self).__init__()


#Parses a line in the following format:
#199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
#returns a list in the following order
#['requester','date','month','day','year','time','hour','minute','second','tz','verb','resource','protocol','response','size']
    def parseLine(self,line):
        record = []

        splits = line.split("- -")
        if len(splits) != 2:
            return -1
        requester = splits[0].strip()
        record.append(requester)
        line = splits[1].strip()
        regexp = re.compile(r"\[(?P<date>[\d]+/[A-Za-z)+/[\d]+)"
                            r":(?P<time>\d\d:\d\d:\d\d)"
                            r" (?P<tz>[\+|\-]\d\d\d\d)\] "
                            )
        result = regexp.search(line)
        if result is None:
            return -1
        else:
            record.append(result.group('date').strip())
            datesplit = result.group('date').split("/")
            record.append(u.getMonthNum(datesplit[1].strip()))
            record.append(datesplit[0].strip())
            record.append(datesplit[2].strip())

            record.append(result.group('time').strip())
            timesplit = result.group('time').split(":")
            record.append(timesplit[0].strip())
            record.append(timesplit[1].strip())
            record.append(timesplit[2].strip())

            record.append(result.group('tz').strip())

            quoteSplits = line.split("\"")
            quotedstr = ""

            # reassemble all of the split pieces except first and last to get the quoted section that contains the
            # HTTP command, requested file\path, and protocol version. It is not true that this will be index 1 of the split
            # because some examples have a " character in the requested file\path
            for x in range(1, len(quoteSplits)-1):
                if x != 1:
                    quotedstr = quotedstr+"\""
                quotedstr = quotedstr + quoteSplits[x]
            quotedstr = quotedstr.strip()

            #get the last piece of the split. This will contain the http response and size of file sent in bytes
            lastPart = quoteSplits[len(quoteSplits)-1].strip() # last part

            regexp = re.compile("(?P<verb>^[A-Z]+)")
            result = regexp.search(quotedstr)
            if(result!= None):
                verb = result.group('verb')
            else:
                verb = ""
            record.append(verb.strip())

            quotedstr = quotedstr[len(verb):].strip() # this removes the http verb leaving the rest of the quoted string for processing
            httpindex = quotedstr.rfind("HTTP/")
            if httpindex == -1:
                resource = quotedstr
                protocol = ""
            else:
                resource = quotedstr[:httpindex]
                protocol = quotedstr[httpindex:]
            record.append(resource.strip())
            record.append(protocol.strip())

            lastPartSplits = lastPart.split(" ")
            record.append(int(lastPartSplits[0].strip())) #http response
            if(len(lastPartSplits)>1):
                record.append(lastPartSplits[1].strip()) # number of bytes sent
            else:
                record.append("")   #number of bytes sent missing
        return record

    #returns the average number of requests per session.
    #requires processSessions has completed
    def avgSession(self):
        sessionSeries = self.sessiondf['total_requests']
        return sessionSeries.astype(int).mean()

    #returns the average size of files sent to clients
    #requires readSingleLineRecordsSemiStructured from the base class has completed
    def avgSize(self):
        sizeSeries = self.df['size']
        hyphensDroped = sizeSeries[sizeSeries != "-"]
        return hyphensDroped.astype(int).mean()

    # returns the minimum size of files sent to clients
    # requires readSingleLineRecordsSemiStructured from the base class has completed
    def minSize(self):
        sizeSeries = self.df['size']
        hyphensDroped = sizeSeries[sizeSeries != "-"]
        return hyphensDroped.astype(int).min()

    # returns the minimum size of files sent to clients
    # requires readSingleLineRecordsSemiStructured from the base class has completed
    def maxSize(self):
        sizeSeries = self.df['size']
        hyphensDroped = sizeSeries[sizeSeries != "-"]
        return hyphensDroped.astype(int).max()

    #creates a second dataframe as a member of the object that contains the following fields
    #['requester', 'date', 'time', 'total_requests']
    def processSessions(self):
        sessionData = []

        requester = ""
        date = ""
        time = ""
        numRequests = 0
        first = True

        for index,row in self.df.iterrows():
            if (row['requester']==requester):
                #another request in the same session
                numRequests += 1
            else:
                if (not first):
                    sessionData.append([requester,date,time,numRequests])
                requester = row['requester']
                date = row['time']
                numRequests = 1
                first = False

        self.sessiondf=DataFrame(sessionData,columns=['requester','date','time','total_requests'])


#these are the calls required to address the parts of project #3
#showing the visualizations is optional and controlled by the parameter
#the filepath of the webserver data is passed in as the 2nd parameter
def assignment3calls(visualize,filepath):
    #setup
    d = serverLog()
    d.readSingleLineRecordsSemiStructured(filepath)

    #1
    print "#1 Access Frequencies for Days of the week"
    d.addDayOfWeek('date', "day_of_week")
    dayFreq = d.frequencies("day_of_week")
    reindexed = dayFreq.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    print reindexed
    print "\n"

    #2
    print "#2 Number of distinct clients and number of requests from each"
    clientFreq = d.frequencies('requester')
    print clientFreq
    print "Distinct Clients Clients: " + str(clientFreq.size)
    print "\n"

    #3
    print "#3 Top 10 pages visited"
    top10 = d.filteredTopNFreq(r"((.html)(:80)?)|(/(\w+)?)(\?([\w,]+))?$", 10, 'resource')
    print top10
    print "\n"

    #4
    print "#4 Min, Max, and Avg file size"
    print "min file size: "+str(d.minSize())
    print "max file size: "+str(d.maxSize())
    print "avg file size: "+str(d.avgSize())
    print "\n"

    #5
    print "#5 Average session lengths"
    d.processSessions()
    print "avg session length "+ str(d.avgSession())+" requests"
    print '/n'


    #6
    if(visualize):
        print "#6 Visualizations"
        values = reindexed.values
        plot.pie(values, labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],autopct='%1.1f%%')
        plot.title("Requests By Day of the Week")
        plot.show()

        x = top10.index
        y = top10.values
        xs = [i + 0.1 for i, _ in enumerate(y)]
        plot.bar(xs, y, align='center', width=0.7)
        plot.xlabel('Page Rank')
        plot.ylabel('Times Requested')
        plot.xticks(xs, range(1, 11))
        plot.title("Top 10 Most Requested Pages (July 1995)")
        plot.show()

        hourFreq = d.frequencies('hour')
        indices = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16",
                   "17", "18", "19", "20", "21", "22", "23"]
        reorder = hourFreq.reindex(indices)
        data = []
        for i in range(8):
            data.append(reorder[i * 3] + reorder[i * 3 + 1] + reorder[i * 3 + 2])
        labels = ['00:00-2:59', '3:00-5:59', '6:00-8:59', '9:00-11:59', '12:00-14:59', '15:00-17:59', '18:00-20:59',
                  '21:00-23:59']

        plot.pie(data, labels=labels, autopct='%1.1f%%')
        plot.title("Requests By Time of Day (July 1995)")
        plot.show()



def main():
    path = raw_input('Enter the file path: ')
    visualize = ''
    while(visualize != "Y" and visualize != "N"):
        visualize = raw_input("Show the visualizations? (Y/N) ")
    if visualize == "Y":
        visualize = True
    elif visualize == "N":
        visualize = False

    assignment3calls(visualize,path)

if __name__ == "__main__":
    main()
