import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv([])

m_cols = ['movie_id', 'title']
movies = pd.read_csv([])

ratings = pd.merge(movies, ratings)

userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')

corrMatrix = userRatings.corr()

corrMatrix = userRatings.corr(method='pearson', min_periods=100)

myRatings = userRatings.loc[0].dropna()

simCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
    # "Adding sims for myRatings.index[i]
    # Retrieve similar movies to this one that I rated
    sims = corrMatrix[myRatings.index[i]].dropna()
    # Now scale its similarity by how well I rated this movie
    sims = sims.map(lambda x: x * myRatings[i])
    # Add the score to the list of similarity candidates
    simCandidates = simCandidates.append(sims)
    
#Glance at our results so far:
# "sorting..."
simCandidates.sort_values(inplace = True, ascending = False)

simCandidates = simCandidates.groupby(simCandidates.index).sum()

simCandidates.sort_values(inplace = True, ascending = False)

filteredSims = simCandidates.drop(myRatings.index)
