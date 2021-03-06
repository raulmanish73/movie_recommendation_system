# -*- coding: utf-8 -*-
"""Movie recommendation project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L8cbesoHQTgBg39Ewh9z6aRHFv8eTuz4
"""

!pip install opendatasets --upgrade --quiet

import opendatasets as od

od.version()

dataset_url = 'https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata'

od.download(dataset_url)

import os

data_dir = '/content/tmdb-movie-metadata'

os.listdir(data_dir)

credits = data_dir + '/tmdb_5000_credits.csv'
movies = data_dir + '/tmdb_5000_movies.csv'

import pandas as pd
import numpy as np

credits_df = pd.read_csv(credits)
movies_df = pd.read_csv(movies)

movies_df.head()

new_df = movies_df.merge(credits_df, on = 'title')

new_df.head()

new_df.info()

final_df = new_df[['movie_id','title','overview','genres','keywords','cast','crew']]

final_df.head()

final_df.genres[0]

final_df.isnull().sum()

final_df.dropna(inplace = True)

import ast

def clean(lst):
  l = []
  for i in ast.literal_eval(lst):
    l.append(i['name'])
  return l

clean('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

final_df['genres'] = final_df['genres'].apply(clean)

final_df['keywords']= final_df['keywords'].apply(clean)

final_df['cast'][0]

def clean1(lst):
  l = []
  counter = 0
  for i in ast.literal_eval(lst):
    if counter !=3: 
      l.append(i['name'])
      counter+=1
    else:
      break
  return l

final_df['cast']

final_df['cast'] = final_df['cast'].apply(clean1)

"""did this step in previous version, to get 5 names"""

final_df['cast'] = final_df['cast'].apply(lambda x: x[0:5])

final_df['crew'][0]

def find_director(lst):
  l = []
  for i in ast.literal_eval(lst):
    if i['job'] == 'Director': 
      l.append(i['name'])
      break
  return l

final_df['crew']= final_df['crew'].apply(find_director)

final_df.head()

final_df['overview'][0].split()

def split(x):
  x.split()

type(final_df['overview'][0])

final_df['overview'].astype(str)

final_df['overview'] = final_df['overview'].apply(lambda x:x.split())

final_df.head()

final_df['genres'] = final_df['genres'].apply(lambda x:[i.replace(' ','') for i in x])
final_df['keywords'] = final_df['keywords'].apply(lambda x:[i.replace(' ','') for i in x])
final_df['cast'] = final_df['cast'].apply(lambda x:[i.replace(' ','') for i in x])
final_df['crew'] = final_df['crew'].apply(lambda x:[i.replace(' ','') for i in x])

final_df.head()

final_df['tags'] = final_df['overview'] + final_df['genres'] + final_df['keywords'] + final_df['cast'] + final_df['crew']

final_df.head()

n_df = final_df[['movie_id','title','tags']]

n_df.head()

n_df['tags'] = n_df['tags'].apply(lambda x:" ".join(x))

n_df

n_df['tags'] = n_df['tags'].apply(lambda x:x.lower())

n_df['tags']

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

word_to_vector = cv.fit_transform(n_df['tags']).toarray()

word_to_vector

cv.get_feature_names()

!pip install nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(i))
  return ' '.join(y)

n_df['tags'] = n_df['tags'].apply(stem)

n_df['tags']

from sklearn.metrics.pairwise import cosine_similarity

list(enumerate(cosine_similarity(word_to_vector)))

similarity = cosine_similarity(word_to_vector)

sorted(list(enumerate(similarity[0])), reverse = True, key = lambda x:x[1])[1:6]

n_df



n_df[n_df['title'] == 'John Carter'].index[0]

def recommend(movie):
  movie_index = n_df[n_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
  
  for i in movies_list:
    print(n_df.iloc[i[0]].title)

n_df.iloc

recommend('El Mariachi')

recommend('Spider-Man 2')

