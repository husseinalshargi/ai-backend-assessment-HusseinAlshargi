from app.services.generate_answer import generate_answer
import datetime

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


if __name__ == "__main__":
    #test_generated_answer()
    test_generated_answer_with_filters()