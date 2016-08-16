# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 18:46
from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.auth.models import User
import pandas as pd


# TODO: Set relative path for import data
def import_data(apps, schema_editor):
    file_path = "/Users/nrogers/Desktop/IronYard/movies/ml-1m/"
    movies = pd.read_csv(file_path + "movies.dat",
                         sep="::",
                         names=['movie_id', 'title', 'genre'],
                         engine='python')

    users = pd.read_csv(file_path + "users.dat",
                        sep="::",
                        names=['user_id', 'gender',
                               'age', 'occupation', 'zip_code'],
                        engine='python')

    ratings = pd.read_csv(file_path + "ratings.dat",
                          sep="::",
                          names=['user_id', 'movie_id', 'score', 'timestamp'],
                          engine='python')
    ratings['ts'] = ratings['timestamp'].apply(
                        lambda x: pd.to_datetime(
                            x * 1000000000).tz_localize('EST'))

    Movie = apps.get_model("movies", "Movie")
    Rating = apps.get_model("movies", "Rating")
    Rater = apps.get_model("movies", "Rater")

    print("Data collected")

    # import movies
    movie_dict = {}
    for index, movie in movies.iterrows():
        mov = Movie(id=movie['movie_id'],
                    title=movie['title'], genre=movie['genre'])
        mov.save()
        movie_dict[mov.id] = mov

    print("Movies imported")

    # import users
    user_dict = {}
    for index, user in users.iterrows():
        usr = User.objects.create_user(username=user['user_id'],
                                       password='password')
        rater = Rater(id=usr.id, gender=user['gender'],
                      age=user['age'], occupation=user['occupation'],
                      zip_code=user['zip_code'], user_id=usr.id)
        rater.save()
        user_dict[rater.id] = rater

    print("Users imported")

    # import ratings
    for index, rating in ratings.iterrows():
        user = user_dict[rating['user_id']]
        movie = movie_dict[rating['movie_id']]
        rtg = Rating(rater=user, movie=movie,
                     timestamp=rating['ts'], score=rating['score'])
        rtg.save()

    print("Ratings imported")


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_data)
    ]
