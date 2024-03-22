import streamlit as st

st.set_page_config(layout="wide")
st.title("OpenAI API WebApp")


st.sidebar.title("AI App")

ai_app = st.sidebar.radio("Choose an AI App", ("Blog generator", "Image Generator", "Movie Recommender"))

if ai_app == "Blog generator":
  st.header("blog generator")
  st.write("prompt to build images")
  topic = st.text_area("Topic", height=30)

elif ai_app == "Image Generator":
  st.header("Image Generatorr")
  st.write("prompt to build images")
  prompt = st.text_area("Topic", height=30)
elif ai_app == "Movie Recommender":
  st.header("Movie Recommender")
  st.write("Describe a movie that you'd like to see.")
  movie_description = st.text_area("Topic", height=30)