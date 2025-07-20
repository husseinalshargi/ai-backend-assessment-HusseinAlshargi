import numpy as np
from sklearn.metrics import pairwise  # to calculate cosine similarity


import app.database as db  # to create a session to interact with the db
from app.models.create_embeddings import embed_text  # to use the embedding model to process the text chunks

session = db.session  

def parse_postgres_embedding(embedding_str):
    #safely parse a PostgreSQL array string to a Python list from a string 
    return list(map(float, embedding_str.strip('{}').split(',')))

def search_semantic(query, filtered_chunks, top_k = 3):
    query_embedding = np.array(embed_text(query)).reshape(1, -1) #reshape to 2D array for cosine similarity calculation

    scored_chunks = []
    for chunk in filtered_chunks:
        # also convert chunk embedding to 2D as as cosine_similarity expects 2D arrays
        chunk_embedding = np.array(parse_postgres_embedding(chunk.embedding)).reshape(1, -1)
        
        similarity = pairwise.cosine_similarity(query_embedding, chunk_embedding)
        scored_chunks.append((similarity, chunk.chunk_text))
    
    #sort by similarity and return top K
    top_chunks = sorted(scored_chunks, key=lambda x: x[0][0], reverse=True)[:top_k] #to sort by similarity in descending order and get the top K chunks

    #return only the chunk texts not the similarity scores
    return [chunk for _, chunk in top_chunks]