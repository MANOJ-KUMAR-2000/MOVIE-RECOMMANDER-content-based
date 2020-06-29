"""
Author @MANOJ_KUMAR_S
Date   29.06.2020
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from PIL import Image,ImageTk
import requests
from io import BytesIO
import tkinter as tk
import random

FULL_MOVIE_DATA = pd.read_csv("IMDb_movies.csv")
small_titlee = [i.lower() for i in FULL_MOVIE_DATA['title']]
FULL_MOVIE_DATA['title'] = small_titlee
FULL_MOVIE_RATING = pd.read_csv("IMDb_ratings1.csv")
FULL_MOVIE_RATING['title'] = small_titlee

data_movies = pd.read_csv("IMDb_movies.csv")
data_movies.sort_values('imdb_title_id', axis=0, inplace=True)
data_movie = data_movies[['imdb_title_id', 'title', 'year','genre', 'language']]


data_ratings = pd.read_csv("IMDb_ratings.csv")
data_ratings.sort_values('imdb_title_id', axis=0, inplace=True)
data_rating = data_ratings[['imdb_title_id', 'weighted_average_vote', 'total_votes', 'mean_vote',
                           'median_vote', 'votes_10', 'votes_9', 'votes_8', 'votes_7', 'votes_6',
                           'votes_5', 'votes_4', 'votes_3', 'votes_2', 'votes_1']]

DATA = pd.concat([data_movie, data_rating.drop('imdb_title_id', axis=1)], axis=1)
N_DATA = DATA
DATA['genre'] = data_movies.genre.str.split(', ')

top_rated_movie = DATA.sort_values('total_votes', ascending=False, axis=0).iloc[:1000,:].reset_index(drop=True)
top_popular = top_rated_movie.iloc[:10,:]
top_worst = DATA.iloc[:30000,:].sort_values("weighted_average_vote", ascending=True, axis=0).reset_index(drop=True).iloc[:10,:]
top_rated_movie = top_rated_movie.sort_values('weighted_average_vote', ascending=False, axis=0).reset_index(drop=True).iloc[:10,:]

TAMIL_MOVIES = DATA[DATA['language'].isin(['Tamil'])]
TAMIL_MOVIES = TAMIL_MOVIES.sort_values('total_votes', ascending=False, axis=0).reset_index(drop=True).iloc[:35,:]
top_rated_tamil = TAMIL_MOVIES.sort_values('weighted_average_vote', ascending=False, axis=0).reset_index(drop=True).iloc[1:11,:].reset_index(drop=True)

global USER_MOVIES
USER_MOVIES = pd.DataFrame([{'imdb_title_id':'tt2199711', 'rating':10}])

def raw_movie_image(movie_id):
    html = urlopen('https://www.imdb.com/title/'+str(movie_id)+'/')
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    url = images[0]['src']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def movie_image(movie_id):
    html = urlopen('https://www.imdb.com/title/'+str(movie_id)+'/')
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    url = images[0]['src']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = ImageTk.PhotoImage(img)
    return img

def recommend_movies(user_profile):
    dummies = pd.read_csv("genre_dummies.csv")
    dummies = dummies.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    genreTable = dummies.set_index(DATA['imdb_title_id'])
    recommendationTable_df = ((genreTable*user_profile).sum(axis=1))/(user_profile.sum())
    recommend_df = pd.DataFrame(recommendationTable_df).reset_index()
    recommend_df.columns = ['imdb_title_id', 'value']
    recomm_movies = DATA.drop(['year'], axis=1)
    recomm_movies['value'] = recommend_df['value'].values
    recomm_movies = recomm_movies.sort_values('value', ascending=False, axis=0).iloc[:2000,:]
    recomm_movies = recomm_movies.sort_values('weighted_average_vote',ascending=False, axis=0).iloc[:1500,:]
    recomm_movies = recomm_movies.sort_values('value', ascending=False, axis=0).iloc[:1000,:]
    recomm_movies = recomm_movies.sort_values('total_votes',ascending=False, axis=0).iloc[:500,:]
    recomm_movies = recomm_movies.sort_values('value', ascending=False, axis=0).iloc[:100,:]
    recomm_movies = recomm_movies.sort_values('total_votes', ascending=False, axis=0).reset_index(drop=True)
    return recomm_movies

def GEN_USER_PROFILE(USER_MOVIES):
    dummies = pd.read_csv("genre_dummies.csv")
    dummies = dummies.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)

    movie_data = pd.concat([data_movie, dummies], axis=1)
    movie_data = movie_data.drop(['year','genre', 'language'], axis=1)

    userMovies = movie_data[movie_data['imdb_title_id'].isin(USER_MOVIES['imdb_title_id'].tolist())]
    user_movie_gener = userMovies.drop(['imdb_title_id','title'], axis=1)
    user_profile = user_movie_gener.transpose().dot(USER_MOVIES['rating'].values)
    return user_profile

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

WINDOW =tk.Tk()
WINDOW.geometry('1000x600')
WINDOW.title('MOVIE Db & RECOMMENDER')
        
img = Image.open('title.png')
img = ImageTk.PhotoImage(img)
title_label = tk.Label(WINDOW,image=img).place(x=325,y=10)

entry = tk.Entry(WINDOW, borderwidth=5)
entry.place(x=25,y=150,height=25,width=300)

def CLEAR():
    try:

        try:
            error_l.destroy()
        except:
            pass
        
        try:
            tr1.destroy()
            tr2.destroy()
            tr3.destroy()
            tr4.destroy()
            tr5.destroy()
            tr6.destroy()
            tr7.destroy()
            tr8.destroy()
            tr9.destroy()
            tr10.destroy()
            tr11.destroy()
            t1.destroy()
            t2.destroy()
            t3.destroy()
            t4.destroy()
            t5.destroy()
            t6.destroy()
            t7.destroy()
            t8.destroy()
            t9.destroy()
            t10.destroy()
            t11.destroy()
        except:
            pass
            
        l1.destroy()
        l2.destroy()
        l3.destroy()
        l4.destroy()
        l5.destroy()
        l6.destroy()
        l7.destroy()
        l8.destroy()
        l9.destroy()
        l10.destroy()
        movie_img_label.destroy()
        l11.destroy()
        l12.destroy()
    except:
        pass

def DISPLAY_RECOMM_MOVIES():
    try:
        rm_img_l1.destroy()
        rm_img_l2.destroy()
        rm_img_l3.destroy()
        rm_img_l4.destroy()
        rm_img_l5.destroy()
        rm_img_l6.destroy()     
    except:
        pass
            
    rm_1_img = raw_movie_image(RECOMMENDED_MOVIES.loc[0]['imdb_title_id'])
    w,h = rm_1_img.size
    rm_1_img = rm_1_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_1_img = ImageTk.PhotoImage(rm_1_img)
    rm_img_l1 = tk.Label(WINDOW, image=rm_1_img)
    rm_img_l1.image=rm_1_img
    rm_img_l1.place(x=500,y=150)
    rm_1= RECOMMENDED_MOVIES.loc[0]['title']
    rb_1 = tk.Button(WINDOW, text=rm_1.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_1.lower()))
    rb_1.place(x=502,y=153+int(h*0.7), width=int(w*0.8), height=15)

    rm_2_img = raw_movie_image(RECOMMENDED_MOVIES.loc[2]['imdb_title_id'])
    w,h = rm_2_img.size
    rm_2_img = rm_2_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_2_img = ImageTk.PhotoImage(rm_2_img)
    rm_img_l2 = tk.Label(WINDOW, image=rm_2_img)
    rm_img_l2.image=rm_2_img
    rm_img_l2.place(x=670,y=150)
    rm_2= RECOMMENDED_MOVIES.loc[2]['title']
    rb_2 = tk.Button(WINDOW, text=rm_2.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_2.lower()))
    rb_2.place(x=672,y=153+int(h*0.7), width=int(w*0.8), height=15)

    rm_3_img = raw_movie_image(RECOMMENDED_MOVIES.loc[4]['imdb_title_id'])
    w,h = rm_3_img.size
    rm_3_img = rm_3_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_3_img = ImageTk.PhotoImage(rm_3_img)
    rm_img_l3 = tk.Label(WINDOW, image=rm_3_img)
    rm_img_l3.image=rm_3_img
    rm_img_l3.place(x=835,y=150)
    rm_3= RECOMMENDED_MOVIES.loc[4]['title']
    rb_3 = tk.Button(WINDOW, text=rm_3.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_3.lower()))
    rb_3.place(x=837,y=153+int(h*0.7), width=int(w*0.8), height=15)

    rm_4_img = raw_movie_image(RECOMMENDED_MOVIES.loc[6]['imdb_title_id'])
    w,h = rm_4_img.size
    rm_4_img = rm_4_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_4_img = ImageTk.PhotoImage(rm_4_img)
    rm_img_l4 = tk.Label(WINDOW, image=rm_4_img)
    rm_img_l4.image=rm_4_img
    rm_img_l4.place(x=500,y=380)
    rm_4 = RECOMMENDED_MOVIES.loc[6]['title']
    rb_4 = tk.Button(WINDOW, text=rm_4.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_4.lower()))
    rb_4.place(x=502,y=383+int(h*0.7), width=int(w*0.8), height=15)

    rm_5_img = raw_movie_image(RECOMMENDED_MOVIES.loc[8]['imdb_title_id'])
    w,h = rm_5_img.size
    rm_5_img = rm_5_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_5_img = ImageTk.PhotoImage(rm_5_img)
    rm_img_l5 = tk.Label(WINDOW, image=rm_5_img)
    rm_img_l5.image=rm_5_img
    rm_img_l5.place(x=670,y=380)
    rm_5= RECOMMENDED_MOVIES.loc[8]['title']
    rb_5 = tk.Button(WINDOW, text=rm_5.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_5.lower()))
    rb_5.place(x=672,y=383+int(h*0.7), width=int(w*0.8), height=15)

    rm_6_img = raw_movie_image(RECOMMENDED_MOVIES.loc[10]['imdb_title_id'])
    w,h = rm_6_img.size
    rm_6_img = rm_6_img.resize((int(w*0.8), int(h*0.7)), Image.ANTIALIAS)
    rm_6_img = ImageTk.PhotoImage(rm_6_img)
    rm_img_l6 = tk.Label(WINDOW, image=rm_6_img)
    rm_img_l6.image=rm_6_img
    rm_img_l6.place(x=835,y=380)
    rm_6= RECOMMENDED_MOVIES.loc[10]['title']
    rb_6 = tk.Button(WINDOW, text=rm_6.upper(), bg='black', fg='#ff9f0f', command=lambda:SEARCH(rm_6.lower()))
    rb_6.place(x=837,y=383+int(h*0.7), width=int(w*0.8), height=15)
       
def TOP_RATED(D_F):
    global t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,tr1,tr2,tr3,tr4,tr5,tr6,tr7,tr8,tr9,tr10,tr11
    CLEAR()
    t1 = tk.Label(WINDOW, text="MOVIES")
    t1.place(x=80,y=200)
    t2 = tk.Label(WINDOW, text=D_F.loc[0]['title'])
    t2.place(x=30,y=225)
    t3 = tk.Label(WINDOW, text=D_F.loc[1]['title'])
    t3.place(x=30,y=250)
    t4 = tk.Label(WINDOW, text=D_F.loc[2]['title'])
    t4.place(x=30,y=275)
    t5 = tk.Label(WINDOW, text=D_F.loc[3]['title'])
    t5.place(x=30,y=300)
    t6 = tk.Label(WINDOW, text=D_F.loc[4]['title'])
    t6.place(x=30,y=325)
    t7 = tk.Label(WINDOW, text=D_F.loc[5]['title'])
    t7.place(x=30,y=350)
    t8 = tk.Label(WINDOW, text=D_F.loc[6]['title'])
    t8.place(x=30,y=375)
    t9 = tk.Label(WINDOW, text=D_F.loc[7]['title'])
    t9.place(x=30,y=400)
    t10 = tk.Label(WINDOW, text=D_F.loc[8]['title'])
    t10.place(x=30,y=425)
    t11 = tk.Label(WINDOW, text=D_F.loc[9]['title'])
    t11.place(x=30,y=450)

    tr1 = tk.Label(WINDOW, text="RATING")
    tr1.place(x=300,y=200)
    tr2 = tk.Label(WINDOW, text=str(D_F.loc[0]['weighted_average_vote']))
    tr2.place(x=325,y=225)
    tr3 = tk.Label(WINDOW, text=str(D_F.loc[1]['weighted_average_vote']))
    tr3.place(x=325,y=250)
    tr4 = tk.Label(WINDOW, text=str(D_F.loc[2]['weighted_average_vote']))
    tr4.place(x=325,y=275)
    tr5 = tk.Label(WINDOW, text=str(D_F.loc[3]['weighted_average_vote']))
    tr5.place(x=325,y=300)
    tr6 = tk.Label(WINDOW, text=str(D_F.loc[4]['weighted_average_vote']))
    tr6.place(x=325,y=325)
    tr7 = tk.Label(WINDOW, text=str(D_F.loc[5]['weighted_average_vote']))
    tr7.place(x=325,y=350)
    tr8 = tk.Label(WINDOW, text=str(D_F.loc[6]['weighted_average_vote']))
    tr8.place(x=325,y=375)
    tr9 = tk.Label(WINDOW, text=str(D_F.loc[7]['weighted_average_vote']))
    tr9.place(x=325,y=400)
    tr10 = tk.Label(WINDOW, text=str(D_F.loc[8]['weighted_average_vote']))
    tr10.place(x=325,y=425)
    tr11 = tk.Label(WINDOW, text=str(D_F.loc[9]['weighted_average_vote']))
    tr11.place(x=325,y=450)
    
def DISPLAY_MOVIE_DETAIL(search_movie):
        global l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,movie_img_label
        searched_movie_detail = FULL_MOVIE_DATA[FULL_MOVIE_DATA['title'].isin([search_movie])].reset_index(drop=True)
        searched_movie_rating = FULL_MOVIE_RATING[FULL_MOVIE_RATING['title'].isin([search_movie])].reset_index(drop=True)
        searched_movie_id = searched_movie_detail.loc[0]['imdb_title_id']
        searched_movie_image = movie_image(searched_movie_id)
        l1 = tk.Label(WINDOW, text='MOVIE TITLE   : %s'%str(searched_movie_detail.loc[0]['title']).capitalize())
        l1.place(x=190,y=200)
        l2 = tk.Label(WINDOW, text='IMDB RATING   : %s'%str(searched_movie_rating.loc[0]['weighted_average_vote']))
        l2.place(x=190,y=230)    
        l3 = tk.Label(WINDOW, text='DIRECTOR      : %s'%str(searched_movie_detail.loc[0]['director']))
        l3.place(x=190,y=260)
        l4 = tk.Label(WINDOW, text='GENRE\'S      : %s'%str(searched_movie_detail.loc[0]['genre']))
        l4.place(x=190,y=290)
        l5 = tk.Label(WINDOW, text='RELEASED YEAR : %s'%str(searched_movie_detail.loc[0]['year']))
        l5.place(x=190,y=320)
        l6 = tk.Label(WINDOW, text='PRODUCTION    : %s'%str(searched_movie_detail.loc[0]['production_company']))
        l6.place(x=190,y=350)
        l7 = tk.Label(WINDOW, text='BUDGET        : %s'%str(searched_movie_detail.loc[0]['budget']))
        l7.place(x=190,y=380)
        l8 = tk.Label(WINDOW, text='GROSS INCOME  : %s'%str(searched_movie_detail.loc[0]['worlwide_gross_income']))
        l8.place(x=190,y=410)
        l9 = tk.Label(WINDOW, text = "PLOT")
        l9.place(x=10,y=460)
        plot_det = searched_movie_detail.loc[0]['description']
        l10 = tk.Label(WINDOW, text=plot_det[:75])
        l10.place(x=10,y=480)
        l11 = tk.Label(WINDOW, text=plot_det[75:149])
        l11.place(x=10,y=500)
        l12 = tk.Label(WINDOW, text=plot_det[149:])
        l12.place(x=10,y=520)
            
        movie_img_label = tk.Label(WINDOW, image=searched_movie_image)
        movie_img_label.image = searched_movie_image
        movie_img_label.place(x=5,y=185)

def SEARCH(search_movie):
    global USER_MOVIES,user_PROFILE,RECOMMENDED_MOVIES,error_l
    if search_movie == "":
        search_movie = entry.get().lower()
    
    CLEAR()   

    if search_movie not in small_titlee:
        error_l = tk.Label(WINDOW, text='NO MOVIE MATCHES ! TRY AGAIN', fg='red')
        error_l.place(x=100,y=180)
    elif search_movie in small_titlee:
        DISPLAY_MOVIE_DETAIL(search_movie)
        searched_movie_detail = FULL_MOVIE_DATA[FULL_MOVIE_DATA['title'].isin([search_movie])].reset_index(drop=True)
        searched_movie_rating = FULL_MOVIE_RATING[FULL_MOVIE_RATING['title'].isin([search_movie])].reset_index(drop=True)
        searched_movie_id = searched_movie_detail.loc[0]['imdb_title_id']
        
        if searched_movie_id not in USER_MOVIES['imdb_title_id'].values:
            new_movie = pd.DataFrame([{'imdb_title_id':searched_movie_id, 'rating':10}])
            USER_MOVIES = USER_MOVIES.append(new_movie, ignore_index=True)

        user_PROFILE = GEN_USER_PROFILE(USER_MOVIES)
        RECOMMENDED_MOVIES = recommend_movies(user_PROFILE)
    DISPLAY_RECOMM_MOVIES()


user_PROFILE = GEN_USER_PROFILE(USER_MOVIES)
RECOMMENDED_MOVIES = recommend_movies(user_PROFILE)


tk.Button(WINDOW, borderwidth=5, bg = 'black', fg='white',text='search', command=lambda:SEARCH("")).place(x=325,y=150, height=25)
top_rated = tk.Button(WINDOW, text='TOP RATED', bg='black', fg='#ff9f0f', command=lambda:TOP_RATED(top_rated_movie))
top_rated.place(x=50,y=10, width=200)
top_tamil = tk.Button(WINDOW, text='சிறந்த தமிழ் படங்கள்', bg='black', fg='#ff9f0f', command=lambda:TOP_RATED(top_rated_tamil))
top_tamil.place(x=50,y=40, width=200)
top_POP_B = tk.Button(WINDOW, text='POPULAR MOVIES', bg='black', fg='#ff9f0f', command=lambda:TOP_RATED(top_popular))
top_POP_B.place(x=50,y=70, width=200)
top_WORST = tk.Button(WINDOW, text='WORST MOVIES', bg='black', fg='#ff9f0f', command=lambda:TOP_RATED(top_worst))
top_WORST.place(x=50,y=100, width=200)
RECOMM_B = tk.Button(WINDOW, text='RECOMMEND MOVIE', bg='black', fg='#ff9f0f', command=lambda:SEARCH(RECOMMENDED_MOVIES.loc[random.randrange(50)]['title'].lower()))
RECOMM_B.place(x=760,y=45, width=200)
creator_l = tk.Label(WINDOW, text='creator @ MANOJ KUMAR S', fg='#a1d5d6')
creator_l.place(x=830,y=10)

WINDOW.mainloop()

