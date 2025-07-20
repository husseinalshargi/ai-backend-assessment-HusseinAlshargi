from app.services.generate_answer import generate_answer
import datetime

from app.services.generate_summary import generate_summary

def test_generated_answer(): 
    #example query
    query = "talk about C# and .NET Fundamentals"
     
    #generate answer
    answer = generate_answer(query)

    #print the generated answer
    print("Generated Answer:", answer)

def test_generated_answer_with_filters():
    #example query with filters
    query = "what is flutter and dart"
    from_date = datetime.date(2025, 7, 8)
    to_date = datetime.date(2025, 7, 25)
    tenant = "public"
    file_name = None

    #generate answer with filters
    answer = generate_answer(query, from_date=from_date, to_date=to_date, tenant=tenant)

    #print the generated answer
    print(answer)

def test_generate_summary():
    #example chat history
    chat_history = [
        {"role": "user", "message": "What is the weather like today?"},
        {"role": "assistant", "message": "The weather is sunny with a high of 25°C."},
        {"role": "user", "message": "What about tomorrow?"},
        {"role": "assistant", "message": "Tomorrow will be cloudy with a chance of rain."}
    ]

    #generate summary
    summary = generate_summary(chat_history)

    #print the generated summary
    print("Generated Summary:", summary)


if __name__ == "__main__":
    #test_generated_answer()
    #test_generated_answer_with_filters()
    test_generate_summary()