import csv
import pandas as pd
import numpy as np
from numpy.linalg import norm

movie_data =  pd.read_csv("movie-lens-data\movie-lens-data/movies.csv")
# print(movie_data)

full_movie_id = movie_data["movieId"]

rating_data = pd.read_csv("movie-lens-data\movie-lens-data/ratings.csv")
sorted_ratings = rating_data.sort_values(by=['userId', 'movieId'])
movie_Ids = sorted_ratings["movieId"].to_numpy()
ratings = sorted_ratings["rating"].to_numpy()
user_Ids = sorted_ratings["userId"].to_numpy()


# This function computes the cosine similarity between two sets of user ratings
def cosine_similarity(A, B):
    temp_A = A
    temp_B = B
    if len(A) > len(B):
        temp_B.extend([0]*(len(A)-len(B)))
    if len(B) > len(A):
        temp_A.extend([0]*(len(B)-len(A)))
    dividend = np.dot(temp_A, temp_B)
    divisor = (norm(temp_A) * norm(temp_B))
    similarity_score = float(dividend)/float(divisor)
    return similarity_score


user_profiles = {}
movie_profiles = {}
for (movie_Id, rating, user_Id) in zip(movie_Ids, ratings, user_Ids):
    user_profiles[(user_Id, movie_Id)] = rating
    if movie_Id in movie_profiles.keys():
        movie_profiles[movie_Id].append(rating)
    else:
        movie_profiles[movie_Id] =  [rating]


similarity_dict = {}
for x in set(movie_profiles.keys()):
    for y in set(movie_profiles.keys()):
        if x is not y and x < y:
            similarity_dict[(x, y)] = cosine_similarity(movie_profiles[x], movie_profiles[y])
            
            
print(similarity_dict)

# user_ratings = [[]]
# for user in user_Ids:
#     index = 0
#     for movie_Id in movie_Ids:
#         user_ratings.append([])
#         if (user, movie_Id) in user_profiles.keys():
#             user_ratings[index].append((movie_Id, user_profiles[(user, movie_Id)]))
#             index = index + 1
#         else:
#             user_ratings[index].append((movie_Id, 0))
#             index = index + 1

# print(user_ratings)

# movie_flag = 0
# for (movie_Id, user_Id) in zip(movie_Ids, user_Ids):
#     if flag != user_Id:
#         flag = user_Id
#         index = index + 1
#         user_ratings.append([])
#     user_ratings[index].append((movie_Id, (user_profiles[(user_Id, movie_Id)])))

# Add zero values for each unrated movie in user ratings
    

# print(cosine_similarity([4,5,0,5,1,0], [0,3,4,3,1,2]))

