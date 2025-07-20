#Tfid will be used to search for keywords in the documents to search for most relevant documents
from sklearn.feature_extraction.text import TfidfVectorizer #to convert text to TF-IDF vectors
import numpy as np

from app.database import sessionlocal
from app.models.document_chunk_record import DocumentChunkRecord

session = sessionlocal()  # create a session to interact with the db

def search_keywords(query, top_k=3):
    #retrive all chunck texts from the database
    chunks = session.query(DocumentChunkRecord).all()
    chunk_texts = [chunk.chunk_text for chunk in chunks]

    if not chunk_texts: #check if there are any document chunks
        print("No document chunks found in the database.")
        return []

    #TF-IDF vectorization
    vectorizer = TfidfVectorizer()

    #fit -> learn, transform -> convert to vectors
    tfidf_matrix = vectorizer.fit_transform(chunk_texts)  
    query_vector = vectorizer.transform([query]) 


    #compute cosine similarity between query and all chunks
    cosine_similarities = (tfidf_matrix * query_vector.T).toarray().flatten()

    #get indices of top_k chunks
    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]
    
    #return the top chunk texts sorted by similarity
    return [chunk_texts[i] for i in top_indices if cosine_similarities[i] > 0]
 