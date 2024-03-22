import streamlit as st
from dotenv import load_dotenv
from ai_functions import generate_blog, generate_images, recommend, chunk_text, insert_vectors, ask_question_on_pdf
from view_support import display_pdf_selector
from pinecone import Pinecone
import os
import uuid 
import streamlit as st

from PyPDF2 import PdfReader


load_dotenv()

## Streamlit: View 
st.set_page_config(layout="wide")
st.title("OpenAI API WebApp")


st.sidebar.title("AI App")

ai_app = st.sidebar.radio("Choose an AI App", ("Blog generator", "Image Generator", "Movie Recommender", "Pdf Chat"))

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

elif ai_app == "Pdf Chat":
  st.header("Pdf Chat")
  st.write("Upload a pdf to chat with the AI")
  uploaded_file = st.file_uploader("Choose a file") 

  if 'pdf_metadata' not in st.session_state:
    st.session_state['pdf_metadata'] = {
      "58477e48-9a92-46a7-bccb-81a18b9a0a2f": "Spice.pdf",
      "fadcede1-c3bf-4ccb-bd62-a7e9e2975503": "Wikipedia.pdf",
    }

  if uploaded_file is not None:
     with st.spinner("Loading..."):
        st.write("Here you go!")
        filename = uploaded_file.name
        pdf_id = str(uuid.uuid4()) 
        st.session_state['pdf_metadata'][pdf_id] = filename
        
        st.write(f"Filename: {filename}, PDF ID: {pdf_id}")

        pdf_reader = PdfReader(uploaded_file)

        text_from_pdf = ""

        for page in range(len(pdf_reader.pages)):
          text_from_pdf += pdf_reader.pages[page].extract_text()

        # st.write(text_from_pdf)

        chunks = chunk_text(text_from_pdf, by='char')
        st.write(chunks)

        insert_vectors(filename, pdf_id, chunks)

        st.write("Done!")

       
  selected_pdf_id = display_pdf_selector()
  if selected_pdf_id:
      question = st.text_input("Ask a question:")
      if question:
          response = ask_question_on_pdf(selected_pdf_id, question)
          st.write(response)  

        
        
