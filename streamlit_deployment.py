import streamlit as st
import os
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("movies")

## AI function 

def generate_blog(topic, platform):
    prompt = f"""
    You are a copywriter specialized in user aquisition, retention, and engagement on social media platform. You are well versed with different formats that gets highest engagement catered to various social platforms.   
    Your task is to write a short impactful copywriting for given topic area.
    Topic Area: {topic}
    Social Platform: {platform}
    """

    response = client.completions.create(
       model="gpt-3.5-turbo-instruct",
       prompt=prompt,
       max_tokens=100,
       temperature=0.5,
    )
    
    return response

## Streamlit: View 
st.set_page_config(layout="wide")
st.title("OpenAI API WebApp")


st.sidebar.title("AI App")

ai_app = st.sidebar.radio("Choose an AI App", ("Blog generator", "Image Generator", "Movie Recommender"))

if ai_app == "Blog generator":
  st.header("blog generator")
  st.write("prompt to build images")
  topic = st.text_area("Topic", height=30)
  platform = st.text_input("Platform", "Instagram")
  if st.button("generate!"):
     st.write("Here you go!")
     response = generate_blog(topic, "Instagram")
     st.text_area("generated blog", value=response.choices[0].text, height=700)

elif ai_app == "Image Generator":
  st.header("Image Generatorr")
  st.write("prompt to build images")
  prompt = st.text_area("Topic", height=30)
  if st.button("generate!"):
    st.write("Here you go!")

elif ai_app == "Movie Recommender":
  st.header("Movie Recommender")
  st.write("Describe a movie that you'd like to see.")

  movie_description = st.text_area("Topic", height=30)

  if st.button("generate!"):
    st.write("Here you go!")