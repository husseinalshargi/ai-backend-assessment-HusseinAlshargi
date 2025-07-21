#Tfid will be used to search for keywords in the documents to search for most relevant documents
from sklearn.feature_extraction.text import TfidfVectorizer #to convert text to TF-IDF vectors
import numpy as np

import app.database as db  
from app.models.document_chunk_record import DocumentChunkRecord

session = db.session  # create a session to interact with the db

def search_keywords(query, filtered_chunks, top_k=3):
    #retrive all chunck texts from the database

    chunk_texts = [chunk.chunk_text for chunk in filtered_chunks]


    #TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    #fit -> learn, transform -> convert to vectors
    tfidf_matrix = vectorizer.fit_transform(chunk_texts)  
    query_vector = vectorizer.transform([query]) 


    #compute cosine similarity between query and all chunks
    cosine_similarities = (tfidf_matrix * query_vector.T).toarray().flatten()

    #get indices of top_k chunks
    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]
    
    # Build result list of dicts with chunk text and file_name only if similarity > 0
    results = []
    for i in top_indices:
        if cosine_similarities[i] > 0:
            chunk = filtered_chunks[i]  # original chunk object
            results.append({
                "chunk": chunk.chunk_text,
                "file_name": chunk.document.file_name
            })

    return results
 