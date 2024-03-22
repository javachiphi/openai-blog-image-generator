import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone



load_dotenv()

client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("movies")

def chunk_text(text, chunk_size=1500, chunk_overlap=100, by='word'):
    if by not in ['word', 'char']:
        raise ValueError("Invalid value for 'by'. Use 'word' or 'char'.")

    chunks = []

    if by == "word":
      text = text.split()
    elif by == 'char':
      text = text
    
    current_chunk_start = 0 
    while current_chunk_start < len(text):
      current_chunk_end = current_chunk_start + chunk_size

      if by == 'word':
        chunk = " ".joint(text[current_chunk_start:current_chunk_end])
      elif by == 'char': 
        chunk = text[current_chunk_start:current_chunk_end]
      
      chunks.append(chunk)
      current_chunk_start += (chunk_size - chunk_overlap)

    return chunks



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


def chunk_text(text, chunk_size=1500, chunk_overlap=100, by='word'):
    if by not in ['word', 'char']:
        raise ValueError("Invalid value for 'by'. Use 'word' or 'char'.")

    chunks = []

    if by == "word":
      text = text.split()
    elif by == 'char':
      text = text
    
    current_chunk_start = 0 
    while current_chunk_start < len(text):
      current_chunk_end = current_chunk_start + chunk_size

      if by == 'word':
        chunk = " ".joint(text[current_chunk_start:current_chunk_end])
      elif by == 'char': 
        chunk = text[current_chunk_start:current_chunk_end]
      
      chunks.append(chunk)
      current_chunk_start += (chunk_size - chunk_overlap)

    return chunks

pcPdf = Pinecone(api_key=os.getenv("PINECONE_PDF_API_KEY"))
pdfIndex = pcPdf.Index("rag-text")

def insert_vectors(filename, pdf_id, chunks):
   for i in range(len(chunks)):
    print(chunks[i])
    print("i", i)

    vector = client.embeddings.create(
        model="text-embedding-ada-002",
        input = chunks[i]
    )

    insert_stats = pdfIndex.upsert(
        vectors=[
            (
                str(i),
                vector.data[0].embedding,
                {
                   "org_text": chunks[i],
                   "filename": filename,
                   "pdf_id": pdf_id,
                }
            )
        ]
    )

    print(insert_stats)


def ask_question_on_pdf(pdf_id, question):
    vector = client.embeddings.create(
        model="text-embedding-ada-002",
        input=question
    )

    result_vector = vector.data[0].embedding

    matches = pdfIndex.query(
        vector=result_vector,
        top_k=1,
        filter={"pdf_id": pdf_id},
        include_metadata=True
    )

    messages = [{"role": "system", "content": """I want you to act as a support agent. Your name is "My Super Assistant". You will provide me with answers from the given info. If the answer is not included, say exactly "Ooops! I don't know that." and stop after that. Refuse to answer any question not about the info. Never break character and always answer on the given text."""}]
    messages.append({"role": "user", "content": matches['matches'][0]['metadata']['org_text']})
    messages.append({"role": "user", "content": question})

    chat_messages = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0,
        max_tokens=400
    )

    result = chat_messages.choices[0].message.content

    return result
