import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("movies")

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




def generate_images(prompt, num_of_images):
  response = client.images.generate(
    prompt=prompt,
    n=num_of_images,
    size="512x512"
  )

  return response


def recommend(movie_description):
    vector = client.embeddings.create(
      model="text-embedding-ada-002",
      input=movie_description
    )

    result_vector = vector.data[0].embedding

    result = index.query(
      vector=result_vector,
      top_k=3,
      include_metadata=True
    )

    return result