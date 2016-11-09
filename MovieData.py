#Matthew Smith
#CS521 Exam 2
#This class is for analysis of MovieLens data

from DataFrameBase import DataFrameBaseType
import datetime
import pandas as pd

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
        mnames = ['movie_id', 'title', 'genres']
        self.movies = pd.read_table(dirpath+'\\movies.dat', sep='::', header=None,names=mnames,engine='python')
        print self.ratings



def main():
    m = MovieData()
    m.loadMovieData('C:\io\ex2')

if __name__ == "__main__":
        main()

#todo work on genres and years for movies
#todo merge frames