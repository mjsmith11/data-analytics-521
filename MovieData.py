#Matthew Smith
#CS521 Exam 2
#This class is for analysis of MovieLens data

from DataFrameBase import DataFrameBaseType
import datetime
import pandas as pd
from pandas import DataFrame,Series
import re
import matplotlib.pyplot as plot
import numpy as np
import utilities as u

class MovieData(DataFrameBaseType):
    def __init__(self):
        self.users = ''
        self.ratings = ''
        self.movies = ''

    def loadMovieData(self,dirpath):
        unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
        self.users = pd.read_table(dirpath+'\\users.dat', sep='::', header=None, names=unames, engine='python')
        rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
        self.ratings = pd.read_table(dirpath+'\\ratings.dat', sep='::', header=None, names=rnames, engine='python')
        self.ratings['datetime'] = self.ratings['timestamp'].map(lambda x: datetime.datetime.fromtimestamp(x))
        self.ratings.drop('timestamp',axis=1,inplace=True)
        mnames = ['movie_id', 'titleandyear', 'genres']
        self.movies = pd.read_table(dirpath+'\\movies.dat', sep='::', header=None,names=mnames,engine='python')
        self.movies['year']=self.movies['titleandyear'].map(lambda mov: self.getMovieYear(mov))
        self.movies['title'] = self.movies['titleandyear'].map(lambda mov: self.getMovieName(mov))
        self.movies.drop('titleandyear',axis=1,inplace=True)
        tempdf = pd.merge(self.users,self.ratings,on='user_id',how='inner')
        self.df = pd.merge(tempdf,self.movies,on='movie_id',how='inner')



    def getMovieYear(self,movieStr):
        searchRes = re.search(r"\(\d\d\d\d\)",movieStr)
        return searchRes.group(0)[1:len(searchRes.group(0))-1] # remove parentheses

    def getMovieName(self,movieStr):
        year = self.getMovieYear(movieStr)
        year = "("+year+")"
        return movieStr[0:movieStr.index(year)-1]

    def getOccupationName(self, code):
        dict = {
            0:"other or not specified",
            1:'academic/educator',
            2:'artist',
            3:'clerical/admin',
            4:'college/grad student',
            5:'customer service',
            6:'doctor/health care',
            7:'executive/managerial',
            8:'farmer',
            9:'homemaker',
            10:'K-12 student',
            11:'lawyer',
            12:'programmer',
            13:'retired',
            14:'sales/marketing',
            15:'scientist',
            16:'self-employed',
            17:'technician/engineer',
            18:'tradesman/craftsman',
            19:'unemployed',
            20:'writer'
        }
        return dict[code]

    #This removes the +4 format from US zip codes
    #if z are zip characters and p are +4 characters, it assumes the following formats
    #Length  5 input: zzzzz
    #Length  9 input: zzzzzpppp
    #Length 10 input: zzzzz-pppp
    #Length  6 input: zzzzzz    Assumed to be non US zip
    #Length  7 input: zzzzzzz   Assumed to be non US zip
    #no other lengths of zips were observed in the file
    def removeZipPlus4(self,zip):
        if len(zip)==9 or len(zip)==10:
            return zip[0:4]
        else:
            return zip

    #basic analytics

    def releaseYearDistribution(self,visualize):
        freq = self.movies['year'].value_counts(sort=False)
        freq.sort_index(inplace=True)
        if (visualize):
            freq.plot.bar()
            plot.title("Movie Distribution by Release Year")
            plot.xlabel("Year")
            plot.ylabel("Movie Count")
            plot.show()
        return freq

    def mostRatedMovies(self,limit):
        return self.filteredTopNFreq(r".*",limit,"title")

    def ratingsEachDayOfWeek(self):
        self.df['weekday']=self.df['datetime'].map(lambda dt: u.getDayStr(dt.weekday()))
        grouped = self.df['rating'].groupby(self.df['weekday'])
        avgRatings = grouped.mean()
        avgRatings.sort_values(inplace=True,ascending=False)
        self.df.drop('weekday',axis=1,inplace=True)
        return avgRatings

    def ReleaseToReviewYears(self):
        self.df['deltaT'] = self.df['datetime'].map(lambda dt: dt.year) - self.df['year'].astype(int)
        dataList = []
        dataList.append(self.df['deltaT'].min())
        dataList.append(self.df['deltaT'].max())
        dataList.append(self.df['deltaT'].mean())
        dataList.append(self.df['deltaT'].std())
        dataList.append(self.df['deltaT'].quantile(0.25))
        dataList.append(self.df['deltaT'].quantile(0.5))
        dataList.append(self.df['deltaT'].quantile(0.75))

        self.df.drop('deltaT',axis=1,inplace=True)
        return Series(dataList,index=['min','max','mean','standard deviation','25%','median','75%'])

    def mostRatedByOccupation(self):
        grouped = self.df['title'].groupby(self.df['occupation'])
        dict = {}
        for code,group in grouped:
            dict[self.getOccupationName(code)] = group.mode().tolist()
        print dict

    #advanced analytics
    def distinctZipCodesAndCounts(self):
        self.df["short_zip"]=self.df['zip'].map(lambda z : self.removeZipPlus4(z))
        res = self.frequencies('short_zip')
        self.df.drop("short_zip",axis=1,inplace=True)
        return res

    def ratingStats(self,visualize):
        result = {}
        grouped = self.df['rating'].groupby(self.df['title'])
        avgRatings = grouped.mean()
        avgRatings.sort_values(inplace=True,ascending=False)

        result['max'] = avgRatings[0]
        maxTitles = []
        for index,val in avgRatings.iteritems():
            if val == result['max']:
                maxTitles.append(index)
            else:
                break
        result['max_titles']=maxTitles

        minTitles=[]
        result['min'] = avgRatings[len(avgRatings)-1]
        for index,val in (avgRatings.reindex(index = avgRatings.index[::-1]).iteritems()):
            if val == result['min']:
                minTitles.append(index)
            else:
                break

        result["min_titles"]=minTitles
        result['mean']=avgRatings.mean()
        result['std']=avgRatings.std()
        result["25%"]=avgRatings.quantile(q=0.25)
        result["50%"] = avgRatings.quantile(q=0.5)
        result["75%"] = avgRatings.quantile(q=0.75)

        if(visualize):
            avgRatings.hist(bins=8)
            plot.title("Movie Rating Distribution")
            plot.xlabel("Average Rating")
            plot.ylabel("Number of Movies")
            plot.show()

        return result

    def bestAndWorstGenres(self):
        genreDummies = self.df['genres'].str.get_dummies() # this is a dataframe indexed the same as self.df and each column is a genre. values are 1 if that index has the genre and 0 if not
        for column in genreDummies:
            genreDummies[column] = genreDummies[column]*self.df['rating'] #0 values are unaffected, 1 values become the rating
        genreDummies = genreDummies.replace(0,np.NaN)
        means = genreDummies.mean(axis=0,skipna=True).sort_values(ascending=False)

        return means

    def occupationGenrePreference(self):
        genreDummies = self.df['genres'].str.get_dummies()  # this is a dataframe indexed the same as self.df and each column is a genre. values are 1 if that index has the genre and 0 if not
        for column in genreDummies:
            genreDummies[column] = genreDummies[column] * self.df['occupation']  # 0 values are unaffected, 1 values become the occupation code
        genreDummies = genreDummies.replace(0, np.NaN)
        return genreDummies.mode(axis=0).ix[0].map(lambda x: self.getOccupationName(x))

    def mostPopularHourByAgeGroup:
        

def main():
    m = MovieData()
    m.loadMovieData('C:\io\ex2')
    #print m.releaseYearDistribution(True)
    #print m.mostRatedMovies(10)
    #x = m.distinctZipCodesAndCounts()
    #print m.bestAndWorstGenres()
    #print m.occupationGenrePreference()
    #print m.ReleaseToReviewYears()
    m.mostRatedByOccupation()

if __name__ == "__main__":
        main()

#todo work on genres
    #print self.movies['genres'].str.get_dummies()