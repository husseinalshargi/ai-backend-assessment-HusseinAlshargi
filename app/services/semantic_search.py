import numpy as np
from sklearn.metrics import pairwise  # to calculate cosine similarity


from app.database import sessionlocal  # to create a session to interact with the db
from app.models.document_chunk_record import DocumentChunkRecord  # to use the model to create a
from app.services.create_embeddings import embed_text  # to use the embedding model to process the text chunks
from app.services.retrive_documents import parse_postgres_embedding  # to parse the embedding from the database

session = sessionlocal()  # create a session to interact with the db



def search_semantic(query, top_k = 3):
    query_embedding = np.array(embed_text(query)).reshape(1, -1) #reshape to 2D array for cosine similarity calculation

    #load all stored chunk embeddings
    chunks = session.query(DocumentChunkRecord).all()
    
    scored_chunks = []
    for chunk in chunks:
        # also convert chunk embedding to 2D as as cosine_similarity expects 2D arrays
        chunk_embedding = np.array(parse_postgres_embedding(chunk.embedding)).reshape(1, -1)
        
        similarity = pairwise.cosine_similarity(query_embedding, chunk_embedding)
        scored_chunks.append((similarity, chunk.chunk_text))
    
    #sort by similarity and return top K
    top_chunks = sorted(scored_chunks, key=lambda x: x[0][0], reverse=True)[:top_k] #to sort by similarity in descending order and get the top K chunks

    #return only the chunk texts not the similarity scores
    return [chunk for _, chunk in top_chunks]