import sqlite3
import wikipedia
import pandas as pd

conn = sqlite3.connect(r'instance/mrs.sqlite')
conn.row_factory = sqlite3.Row #

add_query = 'ALTER TABLE movies ADD COLUMN movie_desc CHAR(200)'
query = 'SELECT title, imdb_url,movie_desc from movies'

curr = conn.cursor()
# movies = curr.execute(query).fetchmany(10)

ratings = curr.execute(
        'SELECT user_id,item_id as movie_id,rating FROM user_ratings'
    ).fetchall()
movies = curr.execute(
    'SELECT id as movie_id,title FROM movies'
).fetchall()
ratings_df = pd.DataFrame(ratings, columns= ['user_id','movie_id','rating'])
movies_df = pd.DataFrame(movies, columns= ['movie_id','title'])
ratings = pd.merge(movies_df, ratings_df)

userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')

# corrMatrix = userRatings.corr()

corrMatrix = userRatings.corr(method='pearson', min_periods=100)
# print(userRatings)
# getting correlated rating by user id
user_id = 38
myRatings = userRatings.loc[user_id].dropna()

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

filteredSims = simCandidates.drop(myRatings.index,errors = 'ignore')
movies_list = list(filteredSims.index)[:5]

query= f"SELECT title, IMDB_URL, Image_URL, movie_desc FROM movies where title in ({','.join(['?']*len(movies_list))})"
topmovies = curr.execute(query, movies_list).fetchall()

import json
j = json.dumps( [dict(ix) for ix in topmovies if ix is not None] )
# not_null_movies = [movie for movie in j if  v is not None in for v in movie.values()]
print(j)
# print(json.dumps(topmovies, indent=4))
#         print(movie)
#         update_query = 'UPDATE movies set IMDB_URL=?, Image_URL=?, movie_desc=? WHERE Title= ?'
#         movie_summary = wikipedia.summary(movie[0], sentences=3)
#         movie_wiki = wikipedia.page(movie[0])
#         movie_thumnail = movie_wiki.images[0]
#         movie_url = movie_wiki.url
#         curr.execute(update_query,(movie_url, movie_thumnail, movie_summary, movie[0]) )
#     except:
#         print(movie[0])
#     finally:
#         conn.commit()
# print('Done')
    
