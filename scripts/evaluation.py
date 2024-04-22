
import pandas as pd
from openai import OpenAI
import re


def ft_response(user_input):

    response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::9CBKKv54",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input}
    ]
    )
    return response.choices[0].message.content

def naive_response(user_input):
    user_input = user_input + " Just give me the answer."

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input},
      {"role": "user", "content": "Just give me the number."}  # Adding the follow-up request
    ]
    )
    return response.choices[0].message.content

def evaluate_ft_responses(test_df):
    correct_num = 0
    for i, row in test_df.iterrows():
        expected_answer = str(row['answer']) # since the ft_response function returns a string
        question = row['question']
        response = ft_response(question)
        if expected_answer == response:
            correct_num += 1
    return correct_num / len(test_df)

def evaluate_naive_responses(test_df):
    correct_num = 0
    for i, row in test_df.iterrows():
        expected_answer = str(row['answer']) # since the naive_response function returns a string
        question = row['question']
        response = naive_response(question)
        # Grab the numerical value from the response since the response contains the reasoning
        pattern = r'\d+'
        numbers = re.findall(pattern, response)
        response = numbers[0]
        if expected_answer == response:
            correct_num += 1
    return correct_num / len(test_df)

if __name__ == '__main__':
    test_df = pd.read_csv('../data/test.csv')
    client = OpenAI(api_key = 'sk-proj-kc7vqqZp4jHbh89EWC25T3BlbkFJRH74KKJyQKpYDijdJpsa')
    print(evaluate_ft_responses(test_df)) 
    print(evaluate_naive_responses(test_df))
    
