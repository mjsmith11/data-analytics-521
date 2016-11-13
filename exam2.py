#Matthew Smith
#CS521 Exam 2
#Quick Console UI
from MovieData import MovieData

def showMenu():
    print "\n"
    print "1. Distribution of Release Years         6. Zip Code Analysis"
    print "2. Most Rated Movies                     7. Average Movie Rating Analysis"
    print "3. Time From Release to Rating           8. Ratings by Genre"
    print "4. Most Rated Movies by Occupation       9. Most Frequent Occupation by Genre"
    print "5. Most Active Time of day by Age       10. Average Ratings By Day of Week"

def getChoice():
    return raw_input("Enter your Choice or 'X' to quit: ")

def getYN(prompt):
    response = ""
    while(response != 'N' and response != 'Y'):
        response = raw_input(prompt+" (Y/N) :")

    return response

def processChoice(choice,md):
    retval = 0
    entertocontinue = 1
    if(choice == '1'):
        choice1(md)
    elif(choice == '2'):
        choice2(md)
    elif (choice == '3'):
        choice3(md)
    elif (choice == '4'):
        choice4(md)
    elif (choice == '5'):
        choice5(md)
    elif (choice == '6'):
        choice6(md)
    elif (choice == '7'):
        choice7(md)
    elif (choice == '8'):
        choice8(md)
    elif (choice == '9'):
        choice9(md)
    elif (choice == '10'):
        choice10(md)
    elif (choice == 'X'):
        retval = 1
        entertocontinue = 0
    else:
        print "Invalid Input! Try again."
        entertocontinue = 0

    if(entertocontinue):
        raw_input("Press Enter to Continue")

    return retval

def choice1(md):
    print "Release Year Distribution"
    vis = getYN("Would you like to see a visualization? ")
    if(vis=='Y'):
        vis = True
    else:
        vis = False
    res = md.releaseYearDistribution(vis)
    res.name = 'Movie Counts'
    res.index.name = 'Release Year'
    print res

def choice2(md):
    print "Most Rated Movies"
    limit = raw_input("How many of the most rated movies would you like to see? ")
    res = md.mostRatedMovies(int(limit))
    res.name = "Movie Rating Count"
    res.index.name = "Title"
    print res

def choice3(md):
    print "Time From Release to Rating"
    res = md.ReleaseToReviewYears()
    res.name = "Release to Rating Years Stats"
    res.index.name = "Statistic"
    print res

def choice4(md):
    print "Most Rated By Occupation"
    res = md.mostRatedByOccupation()
    for index,value in res.iteritems():
        print "\n"+index
        for movie in value:
            print ("    "+movie)
def choice5(md):
    print "Most Active Hour of the Day by Age Group (24 hour)"
    res = md.mostPopularHourByAgeGroup()
    for index,value in res.iteritems():
        printstr = index+":  "
        for hour in value:
            printstr = printstr+str(hour)+" "
        print printstr

def choice6(md):
    print "Zip Code Analysis"
    res = md.distinctZipCodesAndCounts()
    res.name = "Rating Counts"
    res.index.name = "ZIP"
    print res
    print "\nTotal Distinct Zip Codes: "+str(len(res))

def choice7(md):
    print "Average Movie Rating Statistics"
    vis = getYN("Would you like to see a histogram of average ratings? ")
    if (vis == 'Y'):
        vis = True
    else:
        vis = False

    res = md.ratingStats(vis)

    print "min:  "+str(res['min'])
    print "Movies with "+str(res['min'])+" rating"
    for movie in res['min_titles']:
        print "   "+movie

    print "max  :" + str(res['max'])
    print "Movies with " + str(res['max']) + " rating"
    for movie in res['max_titles']:
        print "   " + movie

    print "mean :" + str(res['mean'])
    print "std  :" + str(res['std'])
    print "25%  :" + str(res['25%'])
    print "50%  :" + str(res['50%'])
    print "75%  :" + str(res['75%'])

def choice8(md):
    print "Ratings By Genre"
    res = md.bestAndWorstGenres()
    res.name = "Average Ratings"
    res.index.name = "Genre"
    print res

def choice9(md):
    print "Occupations that Rate Genres the Most"
    res = md.occupationGenrePreference()
    res.name="Most Frequent Occupation"
    res.index.name = "Genre"
    print res

def choice10(md):
    print "Ratings by Day of The Week"
    res = md.ratingsEachDayOfWeek()
    res.name = "Average Rating"
    res.index.name = "Day"
    print res

def main():
    m = MovieData()
    path = raw_input("Enter Path to folder with users.dat, movies.dat, and ratings.dat > ")
    if(path.endswith('\\')):
        path = path[:len(path)-1]
    m.loadMovieData(path)

    quit = 0
    while(not quit):
        showMenu()
        choice = getChoice()
        quit = processChoice(choice,m)


if __name__ == "__main__":
    main()