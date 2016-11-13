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

    #dirpath should be a path to a directory containing users.dat, ratings.dat, and movies.dat without a trailing \
    #this method reads the files and creates a datafram for each file self.users, self.ratings, and self.movies
    #unix timestamps are converted to datetime objects and years are separated from titles.
    #self.df is the result of merging the three dataframes
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


    #returns the year as yyyy from the "movie (year)" string
    def getMovieYear(self,movieStr):
        searchRes = re.search(r"\(\d\d\d\d\)",movieStr)
        return searchRes.group(0)[1:len(searchRes.group(0))-1] # remove parentheses

    #returns the movie title from the "movie (year)" string
    def getMovieName(self,movieStr):
        year = self.getMovieYear(movieStr)
        year = "("+year+")"
        return movieStr[0:movieStr.index(year)-1]

    #returns a string corresponding to the passed occupation code
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

    #returns a string corresponding to the passed age range code
    def getAgeRange(self,code):
        dict = {
            1:"Under 18",
            18:"18-24",
            25:"25-34",
            35:"35-44",
            45:"45-49",
            50:"50-55",
            56:"56+"
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

    #returns a series with years as indices and movies released that year for values
    #shows a barchart visualization if visualize is passed as true
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

    #returns a series with up to limit movies that have the most ratings
    def mostRatedMovies(self,limit):
        return self.filteredTopNFreq(r".*",limit,"title")


    #returns a series with indexes ['min','max','mean','standard deviation','25%','median','75%'] and values representing these statistics for time in years between movie release and reviews
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

    #returns a series indexed by occupation strings and contains values that are python lists of the most frequently reviewed movie by that occupation
    #the list is required for bimodal data
    def mostRatedByOccupation(self):
        grouped = self.df['title'].groupby(self.df['occupation'])
        dict = {}
        for code,group in grouped:
            dict[self.getOccupationName(code)] = group.mode().tolist()
        return Series(dict)

    #returns a series indexed by age group strings with values of the most common hour for that age group
    #values are python list objects in order to accomdate bimodal data
    def mostPopularHourByAgeGroup(self):
        self.df['hour']=self.df['datetime'].map(lambda dt: dt.hour)
        grouped = self.df['hour'].groupby(self.df['age'])
        dict = {}
        for age,group in grouped:
            dict[self.getAgeRange(age)]=group.astype(int).mode().tolist()
        self.df.drop('hour',axis=1,inplace=True)
        return Series(dict)

    #advanced analytics

    #returns a series indexed by zipcodes with the +4 digits removed for US zips and values counting reviews from that zip
    def distinctZipCodesAndCounts(self):
        self.df["short_zip"]=self.df['zip'].map(lambda z : self.removeZipPlus4(z))
        res = self.frequencies('short_zip')
        self.df.drop("short_zip",axis=1,inplace=True)
        return res


    #returns a python dictionary of stats calculated on each movie's average rating
    #keys are max,max_titles,min,min_titles,mean,std,25%,50%,75%
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

    #this returns a series indexed by genre names with average ratings for that genre as values
    def bestAndWorstGenres(self):
        genreDummies = self.df['genres'].str.get_dummies() # this is a dataframe indexed the same as self.df and each column is a genre. values are 1 if that index has the genre and 0 if not
        for column in genreDummies:
            genreDummies[column] = genreDummies[column]*self.df['rating'] #0 values are unaffected, 1 values become the rating
        genreDummies = genreDummies.replace(0,np.NaN)
        means = genreDummies.mean(axis=0,skipna=True).sort_values(ascending=False)

        return means

    #returns a series indexed by genre and values are names of occupations that reviewd that genre most
    def occupationGenrePreference(self):
        genreDummies = self.df['genres'].str.get_dummies()  # this is a dataframe indexed the same as self.df and each column is a genre. values are 1 if that index has the genre and 0 if not
        for column in genreDummies:
            genreDummies[column] = genreDummies[column] * self.df['occupation']  # 0 values are unaffected, 1 values become the occupation code
        genreDummies = genreDummies.replace(0, np.NaN)
        return genreDummies.mode(axis=0).ix[0].map(lambda x: self.getOccupationName(x))


    #teturns a series indexed by day of the week and values representing the average rating given on that day
    def ratingsEachDayOfWeek(self):
        self.df['weekday']=self.df['datetime'].map(lambda dt: u.getDayStr(dt.weekday()))
        grouped = self.df['rating'].groupby(self.df['weekday'])
        avgRatings = grouped.mean()
        avgRatings.sort_values(inplace=True,ascending=False)
        self.df.drop('weekday',axis=1,inplace=True)
        return avgRatings
