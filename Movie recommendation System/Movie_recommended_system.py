import pickle
import pandas as pd
import streamlit as st
import difflib

# Loading the data into pd
movie_data = pd.read_csv("C:/Users/user/Desktop/Movie recommendation System/movies.csv")

# Loading the saved model
movie_model = pickle.load(open("C:/Users/user/Desktop/Movie recommendation System/movie_trained.sav", 'rb'))

def get_recommendations(movie_name):
    list_of_all_titles = movie_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_title = movie_data[movie_data.title == close_match]['index'].values[0]

        similarity_score = list(enumerate(movie_model[index_of_the_title]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommended_movies = []
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movie_data[movie_data.index == index]['title'].values[0]
            recommended_movies.append(title_from_index)
            if len(recommended_movies) >= 30:
                break

        return recommended_movies

    return []

# Create the Streamlit web app
def main():
    # Set page title and favicon
    st.set_page_config(page_title='Movie Recommendation System', page_icon='🎥')


    # Sidebar input for movie title
    st.sidebar.title('Movie Recommendation System')
    movie_name = st.sidebar.text_input('Enter Your Favorite Movie Name:', '')

    # Display the selected movie name
    st.subheader('Movie Selected:')
    st.markdown(f"**{movie_name}**")

    # Get movie recommendations
    recommended_movies = get_recommendations(movie_name)

    # Display the recommended movies
    st.subheader('Movies Suggested For You:')
    if recommended_movies:
        for i, movie in enumerate(recommended_movies):
            st.markdown(f"{i + 1}. {movie}")
    else:
        st.info('No recommendations found.')

if __name__ == '__main__':
    main()
