import streamlit as st
from dotenv import load_dotenv
from ai_functions import generate_blog, generate_images, recommend

load_dotenv()

## Streamlit: View 
st.set_page_config(layout="wide")
st.title("OpenAI API WebApp")


st.sidebar.title("AI App")

ai_app = st.sidebar.radio("Choose an AI App", ("Blog generator", "Image Generator", "Movie Recommender"))

if ai_app == "Blog generator":
  st.header("blog generator")
  st.write("prompt to build images")
  topic = st.text_area("Topic", height=30)
  platform = st.text_input("Social Platform", "Instagram")
  if st.button("generate!"):
    with st.spinner("Loading..."):
     st.write("Here you go!")
     response = generate_blog(topic, platform)
     st.text_area("generated blog", value=response.choices[0].text, height=700)

elif ai_app == "Image Generator":
  st.header("Image Generatorr")
  st.write("prompt to build images")
  prompt = st.text_area("Prompt", height=30)
  num_of_images = st.slider("Number of images", 1, 3, 1)

  if st.button("generate!") and prompt != "":
     with st.spinner("Loading..."):
        st.write("Here you go!")

        response = generate_images(prompt, num_of_images)

        for output in response.data:
          st.image(output.url)

elif ai_app == "Movie Recommender":
  st.header("Movie Recommender")
  st.write("Describe a movie that you'd like to see.")

  movie_description = st.text_area("Topic", height=30)

  if st.button("generate!") and movie_description != "":
    with st.spinner("Loading..."):
      st.write("Here you go!")

      result = recommend(movie_description)

      for movie in result.matches:
        st.write(movie.metadata["title"])