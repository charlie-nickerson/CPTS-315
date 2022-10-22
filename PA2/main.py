import csv
import pandas as pd
import numpy as np
import time
import json
from numpy.linalg import norm

movie_data =  pd.read_csv("movie-lens-data\movie-lens-data/movies.csv")

debugging_data = pd.read_csv("similarity-matrix-debugging-information.csv")

print(type(debugging_data))
print(debugging_data)

# print(movie_data)

full_movie_id = movie_data["movieId"]



rating_data = pd.read_csv("movie-lens-data\movie-lens-data/ratings.csv")
sorted_ratings = rating_data.sort_values(by=['userId', 'movieId'])
movie_Ids = sorted_ratings["movieId"].to_numpy()
ratings = sorted_ratings["rating"].to_numpy()
user_Ids = sorted_ratings["userId"].to_numpy()

# Got from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# This function computes the cosine similarity between two sets of user ratings
def cosine_similarity(A, B):
    temp_A = center([i[1] for i in A])
    temp_B = center([i[1] for i in B])
    dividend = np.dot(temp_A, temp_B)
    divisor = (norm(temp_A) * norm(temp_B))
    # if divisor == 0:
    #     return 0
    similarity_score = float(dividend)/float(divisor)
    return similarity_score

# Takes the sum of all the non zero values from lst.
# Subtracts the average of the non zero values
# Subtracts the average from each non zero value in lst
def center(lst):
    sum = 0
    nsum = 0
    count = 0
    for e in lst:
        if e == 0:
            continue
        else:
            sum = sum+e
            count = count+1
    nlst = list(map( lambda x: 0 if (x == 0) else x - sum/float(count), lst))
    
    for e in nlst:
        nsum = e + nsum
    if nsum == 0 or count == 1:
        return lst
    else:
        return nlst


# Puts every user into a dictionairy
# the key is the movie_Id and the value is (movie_Id, rating)
user_dict = {}
for (movie_Id, rating, user_Id) in zip(movie_Ids, ratings, user_Ids):
    if user_Id in user_dict.keys():
        user_dict[user_Id].append((movie_Id, rating))
    else:
        user_dict[user_Id] =  [(movie_Id, rating)]



delete = [key for key in user_dict if len(user_dict[key]) < 1500]

for key in delete:
    del user_dict[key]

Profiles = {}
for user in user_dict.keys():
    for pair in user_dict[user]:
        if pair[0] in Profiles.keys():
            Profiles[pair[0]].append((user, pair[1]))
        else:
            Profiles[pair[0]] = [(user, pair[1])]

# print(Profiles)

# Puts every movie into a dictionairy
# the key is the movie_Id and the value is (user_Id, rating)
# Profiles = {}
# for (movie_Id, rating, user_Id) in zip(movie_Ids, ratings, user_Ids):
#     if movie_Id in Profiles.keys():
#         Profiles[movie_Id].append((user_Id, rating))
#     else:
#         Profiles[movie_Id] =  [(user_Id, rating)]

# for key in Profiles.keys():
#     if sum([i[1] for i in Profiles[key]]) == 0:
#         del Profiles[key]


def fill_list(list1, list2):
    key1 = [i[0] for i in list1]

    for j in list2:
        if j[0] in key1:
            continue
        else:
            list1.append((j[0], 0))
    return list1



# similarity_dict = {}
# l = len(Profiles.keys())
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, u1 in enumerate(Profiles.keys()):
#     for u2 in Profiles.keys():
#         if (u1 >= u2):
#             continue
#         else:
#             nlist1 = sorted(fill_list(Profiles[u1], Profiles[u2]), key=lambda x: x[0])
#             nlist2 = sorted(fill_list(Profiles[u2], Profiles[u1]), key=lambda x: x[0])
#             similarity_dict[(u1,u2)] = cosine_similarity(nlist1, nlist2)
#     time.sleep(0.1)
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

# print(similarity_dict)


            

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

