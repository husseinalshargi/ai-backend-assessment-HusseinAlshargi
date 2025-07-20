import json #to convert the data from json format to dict
import app.database as db  #to access the database session and redis instance
from app.models.conversation_summary import ConversationSummary
from app.services.generate_summary import generate_summary  #to access the ConversationSummary model

session = db.session  #create a session to interact with the db

#short term memory (saved in redis) to store the conversation context
short_term_prefix = "conversation:" #prefix for short term memory keys
short_term_limit = 10  #limit the number of messages in short term memory

summarize_turns = 10  #number of turns to summarize the conversation


#store a message in the short term memory
def store_message(conversation_id, role, message):
    key = f"{short_term_prefix}{conversation_id}"
    messages = db.r.lrange(key, 0, -1)  #retrieve all messages
    if len(messages) >= short_term_limit:
        db.r.lpop(key)  #remove the oldest message if limit is reached for example if the limit is 5, the 6th message will remove the first one
    db.r.rpush(key, json.dumps({"role": role, "message": message}))  #store the new message as a json string

    #store a summary from the long term memory if the number of messages is a multiple of short_term_limit
    if db.r.llen(key) % summarize_turns == 0:
        #if the number of messages is a multiple of summarize_turns, store a summary in long term memory, store the last 10 messages for summarization
        history = [json.loads(m) for m in db.r.lrange(key, 0, -1)] #convert messages from json format to dict, it will be a list of dicts
        summary = generate_summary(history)  #generate the summary
        #store the summary in the redis database
        store_summary(conversation_id, summary, db.r.llen(key))

#get the conversation history from short term memory
def get_context(conversation_id):
    key = f"{short_term_prefix}{conversation_id}"
    messages = db.r.lrange(key, 0, -1)  #retrieve all messages
    return [json.loads(m) for m in messages]  #convert the messages from json format to dict


#long term memory (saved in the database) to store the conversation summary
def store_summary(conversation_id, summary, turn_number):
    #create a new record in the database
    record = ConversationSummary(
        conversation_id=conversation_id,
        summary=summary,
        turn_number=turn_number
    )
    session.add(record)  #add the record to the session
    session.flush()  #flush the session to ensure the record is added to the db
    session.commit()  #commit the session to save the changes to the db

    #make sure to store the summary turn number in short term memory as well
    redis_key = f"summary:{conversation_id}:{turn_number}"
    db.r.set(redis_key, summary)

#get all summaries for a conversation
def get_summaries(conversation_id):
    records = session.query(ConversationSummary).filter_by(conversation_id=conversation_id).all()  #retrieve all records for the conversation
    return [{"id": r.id, "summary": r.summary, "turn_number": r.turn_number} for r in records]  #return a list of summaries with their ids and turn numbers