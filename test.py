from app.services.generate_answer import generate_answer
def test_generated_answer():
    
    # Example query
    query = "talk about C# and .NET Fundamentals"
    
    # Generate answer
    answer = generate_answer(query)
    
    # Print the generated answer
    print("Generated Answer:", answer)




if __name__ == "__main__":
    test_generated_answer()