#Tfid will be used to search for keywords in the documents to search for most relevant documents
from sklearn.feature_extraction.text import TfidfVectorizer #to convert text to TF-IDF vectors
import numpy as np

from app.database import sessionlocal
from app.models.document_chunk_record import DocumentChunkRecord

session = sessionlocal()  # create a session to interact with the db

def search_keywords(query, filtered_chunks, top_k=3):
    #retrive all chunck texts from the database

    #TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    #convert the filtered chunks to strings
    filtered_chunks = [chunk.chunk_text for chunk in filtered_chunks] 

    #fit -> learn, transform -> convert to vectors
    tfidf_matrix = vectorizer.fit_transform(filtered_chunks)  
    query_vector = vectorizer.transform([query]) 


    #compute cosine similarity between query and all chunks
    cosine_similarities = (tfidf_matrix * query_vector.T).toarray().flatten()

    #get indices of top_k chunks
    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]
    
    #return the top chunk texts sorted by similarity
    return [filtered_chunks[i] for i in top_indices if cosine_similarities[i] > 0]
 