import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '4fa07c4a92653c00035e71525e3aef95'
tmdb.language = 'ko-KR'

movies = pickle.load(open('movies.pickle' , 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

def get_recommendations(title):
    #제목을 통해서 영화의 인덱스 값을 얻기
    idx = movies[movies['title'] == title].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)#코사인 유사도 기준으로 내림차순 정렬
    
    sim_scores = sim_scores[1:11] # 내림차순 정렬에서 자기 자신을 제외한 10개의 영화 슬라이싱
    
    #추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices= [i[0] for i in sim_scores]
    
    # 인덱스 정보를 통해 영화 제목 추출
    images = []
    titles = []
    for i in movie_indices :
        id = movies['id'].iloc[i]
        details = movie.details(id)
        
        image_path = details['poster_path']
        if image_path :
            image_path = 'https://image.tmdb.org/t/p/w500'+ details['poster_path']
        else:
            image_path = 'no_image.jpg'
            
        
        images.append(image_path)
        titles.append(details['title'])
        
    return images, titles



st.set_page_config(layout = 'wide')
st.header('MyMVsite')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend') :
    with st.spinner('Please wait...') :
        images, titles = get_recommendations(title)
    
        idx = 0
        for i in range(0, 2) :
            cols = st.columns(5)
            for col in cols :
                col.image(images[idx])
                col.write(titles[idx])
                idx +=1