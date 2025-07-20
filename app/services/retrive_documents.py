from app.database import sessionlocal #to create a session to interact with the db
from app.services.semantic_search import search_semantic  # to use semantic search
from app.services.keyword_search import search_keywords  # to use keyword search

from collections import defaultdict #in order to create a dict that can provide default values when a key is not found


session = sessionlocal() #create a session to interact with the db
RRF_K = 60 #to caalculate the RRF score -> Reciprocal Rank Fusion

#a function to retrieve relevant chunks of both semantic and keyword search then return the top K chunks based on RRF score
def reciprocal_rank_fusion(semantic_results, keyword_results, top_k=3): 
    scores = defaultdict(float) #default is 0.0 for any key not found

    #get RRF scores to semantic results
    for rank, text in enumerate(semantic_results):
        scores[text] += 1 / (RRF_K + rank)

    #get RRF scores to keyword results
    for rank, text in enumerate(keyword_results):
        scores[text] += 1 / (RRF_K + rank)

    # Sort chunks by combined RRF score
    ranked_chunks = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Return top_k chunk texts
    return [text for text, _ in ranked_chunks[:top_k]]

def parse_postgres_embedding(embedding_str):
    # safely parse a PostgreSQL array string to a Python list
    return list(map(float, embedding_str.strip('{}').split(',')))

def retrieve_relevant_chunks(query, top_k = 3):
    # Get semantic & keyword-based chunks
    semantic_chunks = search_semantic(query, top_k=top_k * 2)  
    keyword_chunks = search_keywords(query, top_k=top_k * 2)

    # Apply RRF to combine both
    fused_chunks = reciprocal_rank_fusion(semantic_chunks, keyword_chunks, top_k=top_k)

    return fused_chunks
