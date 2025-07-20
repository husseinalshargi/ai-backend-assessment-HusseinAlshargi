import json #to convert the data from json format to dict
import app.database as db  #to access the database session and redis instance
from app.models.conversation_summary import ConversationSummary  #to access the ConversationSummary model

session = db.session  #create a session to interact with the db

#short term memory (saved in redis) to store the conversation context
short_term_prefix = "conversation:" #prefix for short term memory keys
short_term_limit = 5  #limit the number of messages in short term memory

summarize_turns = 10  #number of turns to summarize in long term memory

#store a message in the short term memory
def store_message(conversation_id, role, message):
    key = f"{short_term_prefix}{conversation_id}"
    messages = db.r.lrange(key, 0, -1)  #retrieve all messages
    if len(messages) >= short_term_limit:
        db.r.lpop(key)  #remove the oldest message if limit is reached for example if the limit is 5, the 6th message will remove the first one
    db.r.rpush(key, json.dumps({"role": role, "message": message}))  #store the new message


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