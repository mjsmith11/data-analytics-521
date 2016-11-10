#Matthew Smith
#CS521 Exam 2
#This class is for analysis of MovieLens data

from DataFrameBase import DataFrameBaseType
import datetime
import pandas as pd
import re

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




def main():
    m = MovieData()
    m.loadMovieData('C:\io\ex2')

if __name__ == "__main__":
        main()

#todo work on genres
    #print self.movies['genres'].str.get_dummies()