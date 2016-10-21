# coding=utf-8
#199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
import re
import pandas as pd
import numpy as np
import utilities as u
from pandas import Series,DataFrame
from DataFrameBase import DataFrameBaseType

class serverLog(DataFrameBaseType):
    def __init__(self):
        self.columnNames = ['requester','date','month','day','year','time','hour','minute','second','tz','verb','resource','protocol','response','size']
        super(serverLog,self).__init__()

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




def main():
    d = serverLog()
    d.readSingleLineRecordsSemiStructured("C:\\io\\access_log_Jul95")
    print d.df.ix[3]
if __name__ == "__main__":
    #print parseLine("199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] \"GET /history/apollo/ HTTP/1.0\" 200 6245")
    #print parseLine("pipe6.nyc.pipeline.com - - [01/Jul/1995:00:22:43 -0400] \"GET /shuttle/missions/sts-71/movies/sts-71-mir-dock.mpg\" 200 946425")
    main()
    #print parseLine("firewall.dfw.ibm.com - - [20/Jul/1995:07:53:24 -0400] \"1/history/apollo/images/\" 400 -")
    #print parseLine("p12.haifa1.actcom.co.il - - [07/Jul/1995:17:49:26 -0400] \"GET /shuttle/resources/orbiters/†b×	 HTTP/1.0\" 404 -")
    #print parseLine("202.251.172.60 - - [14/Jul/1995:04:10:23 -0400] \"GET /shuttle/missions/sts-65/mission-sts-65.htmlhþ§Š ’žŽ‡||(­ HTTP/1.0\" 404 -")