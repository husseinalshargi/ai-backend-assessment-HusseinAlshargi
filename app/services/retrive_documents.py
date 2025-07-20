from app.database import sessionlocal #to create a session to interact with the db
from app.models.document_chunk_record import DocumentChunkRecord
from app.models.ingested_file_record import IngestedFileRecord  # to use the model to filter chunks
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


def get_filtered_chunks(from_date=None, to_date=None, tenant=None, file_name=None):
    session = sessionlocal()  # create a session to interact with the db
    query = session.query(DocumentChunkRecord).join(IngestedFileRecord, DocumentChunkRecord.document_id == IngestedFileRecord.id).distinct()  #join to get the file metadata

    #apply filters based on provided parameters
    if from_date:
        query = query.filter(IngestedFileRecord.process_date >= from_date)
    if to_date:
        query = query.filter(IngestedFileRecord.process_date <= to_date)
    if tenant:
        query = query.filter(IngestedFileRecord.tenant == tenant)
    if file_name:
        query = query.filter(IngestedFileRecord.file_name == file_name)
    chunks = query.all()
    return chunks


def retrieve_relevant_chunks(query, top_k = 3, from_date=None, to_date=None, tenant=None, file_name=None):
    #get filtered chunks based on the provided parameters
    filtered_chunks = get_filtered_chunks(from_date, to_date, tenant, file_name)

    if not filtered_chunks:
        print("No relevant chunks found based on your filters.")
        return []

    #get semantic and keyword searched chunks
    semantic_chunks = search_semantic(query, filtered_chunks, top_k=top_k * 2)  
    keyword_chunks = search_keywords(query, filtered_chunks, top_k=top_k * 2)

    #apply RRF to combine both
    fused_chunks = reciprocal_rank_fusion(semantic_chunks, keyword_chunks, top_k=top_k)

    return fused_chunks
