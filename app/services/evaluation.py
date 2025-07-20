import json
import time
import datetime 
import numpy as np
from sklearn.metrics import pairwise  # to calculate cosine similarity
from pathlib import Path 
import re 

from app.retrieval import generate_answer, create_embeddings

def extract_numbers(text):
    return re.findall(r'\d{4}|\d+', text) #4 digit numbers (years) or any number

def hallucination_check(expected, actual):
    expected_nums = set(extract_numbers(expected))
    actual_nums = set(extract_numbers(actual))
    return expected_nums == actual_nums #return True if the numbers match, False otherwise

def evaluate_answer(question_key = "question", correct_answer_key = "expected"):
    benchmark_question_path = Path("benchmark/questions.json")  
    report_path = Path("benchmark/evaluation_report.md") #markdown report for the evaluation

    with open(benchmark_question_path, "r") as file:
        benchmark_questions = json.load(file) #load questions from the json file for testing (evaluation)
    
    #after loading the questions, we can start the evaluation
    evaluation_results = []  #to store the evaluation results for each question to generate a report later
    for query in benchmark_questions:
        question = query[question_key]
        correct_answer = query[correct_answer_key]

        #generate the answer using the AI assistant
        start_time = time.time()  #start time submitting the query 
        generated_answer = generate_answer.generate_answer(question)  #generate the answer using the AI assistant
        end_time = time.time()  #end time for performance evaluation

        lastency_ms = round((end_time - start_time) * 1000, 4)  #convert to milliseconds

        #evaluate the generated answers

        #calculate embedding similarity
        answer_embedding = create_embeddings.embed_text(generated_answer)
        correct_answer_embedding = create_embeddings.embed_text(correct_answer)
        similarity = pairwise.cosine_similarity(np.array(answer_embedding).reshape(1, -1), np.array(correct_answer_embedding).reshape(1, -1))[0][0] #we used [0][0] to get the similarity value from the 2D array returned by cosine_similarity
        similarity_percentage = round(similarity * 100, 2)

        #check for hallucination
        hallucinated = not hallucination_check(generated_answer, correct_answer)


        evaluation_results.append({
            "question": question,
            "expected": correct_answer,
            "generated": generated_answer,
            "similarity": similarity_percentage,
            "latency_ms": lastency_ms,
            "hallucinated": hallucinated
        })
    
    #generate the evaluation report
    with open(report_path, "w") as report_file:
        report_file.write("Evaluation Report\n")
        report_file.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for result in evaluation_results:
            report_file.write(f"Question: {result['question']} \nExpected Answer: {result['expected']} \nGenerated Answer: {result['generated']} \nSimilarity: {result['similarity']}% \nLatency: {result['latency_ms']} \nHallucinated: {'Yes' if result['hallucinated'] else 'No'} \n ------------------------------------------------------------------\n")
        
        report_file.write("\n")

        avg_sim = sum(r["similarity"] for r in evaluation_results) / len(result)
        avg_lat = sum(r["latency_ms"] for r in evaluation_results) / len(result)
        hallu_rate = sum(1 for r in evaluation_results if r["hallucinated"]) / len(result)
        hallu_percentage = round(hallu_rate * 100, 2)

        report_file.write(f"Average Similarity: {round(avg_sim, 4)}\n\n")
        report_file.write(f"Average Latency: {round(avg_lat, 2)} ms\n\n")
        report_file.write(f"Hallucination Rate: {hallu_percentage}%\n")

        print("Evaluated succesfully")






