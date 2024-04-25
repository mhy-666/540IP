# Reverse Math Solver

## Project Overview
Current model like GPT doesn’t do a very good job on a lot of math problems without using chain of thought (COT), especially for reverse math problems. Even though using COT, it generates answer slowly and not always accurate. Thus, this project aims to improve the performance of GPT 3.5-Turbo without using COT by a dataset of reverse math problems. We will use a dataset of reverse math problems and fine-tune GPT 3.5-Turbo on it to generate more accurate and efficient answers.

### How to run the project locally
#### Environment Requirements
- Python 3.8+
- Required dependencies (see requirements.txt)

#### Installation Steps
After you fork and git clone the project, You should do the following steps:
1. Prepare for the virtual environment `python -m venv venv`
2. Activate virtual environment.<br/> Windows:`venv\Scripts\activate`, MacOS or Linux:`source venv/bin/activate`
3. Install required packages `pip install -r requirements.txt`

### What is Reverse Math Problem?
Normal math problems require forward thoughts. Here's an example of Q & A pair for forward math problem:
- **Q**: James buys 5 packs of beef that are 4 pounds each. The price of beef is $5.50 per pound. How much did he pay? 
- **A** He bought 5*4=20 pounds of beef. So he paid 20 * 5.5 = $110. The answer is: 110 (Using COT) 

On the other hand, reverse math problems require backward thinking. Here's an example of reverse math problem:
- James buys x packs of beef that are 4 pounds each. The price of beef is $5.50 per pound. How much did he pay? If we know the answer to the above question is 110, what is the value of unknown variable x?

### Model Train

#### 1. Machine Learning model - N-gram Model

The n-gram model is a type of language model that predicts the next word by statistically analyzing the frequency of sequences of n words (i.e., n-grams) in the text. For example, a 2-gram (or bigram) model would consider sequences of every two words, while a 3-gram (or trigram) model would consider sequences of every three words. The steps is summarized below:

1. **Data Loading and Processing**: Through the `load_data` method, data is loaded from a specified CSV file, containing the questions and answers. The loaded data is stored in a Pandas DataFrame for easy subsequent processing.

2. **Text Tokenization**: In the `tokensize` method, all questions are first combined into a longer string, then tokenized into a list of words using the `nltk` `word_tokenize` method. This step converts the text into a sequence of words that can be further analyzed.

4. **Generating Bigrams**: Using the `generate_bigrams` method, the cleaned word sequence is converted into bigrams (word pairs), providing the model with the ability to consider the adjacent relationships between words. At the same time, the frequency distribution of bigrams is calculated and stored, which is very useful for understanding the relationships between words and generating text.

5. **Text Generation**: The `generate_text` method starts by randomly selecting a bigram as the starting point. Then, based on the second word of the current bigram, it finds all possible subsequent words and randomly selects one as the next word. Thus generation exists some randomness and uncertainty.

#### 2. Deep Learning Approach - Fine tune OpenAI gpt 3.5-Turbo
1. **Data loading**: Load dataset from the json file `training_data.jsonl` Data is in the format of :

```
{
    "messages":[
    {"role":"system","content":"\n You are a clever  
    mathematician. \n Please give me the answer of the 
    given questions. \n "},
    {"role":"user","content":"Bud makes homemade 
    macaroni and cheese once a week.  The pasta costs 
    $1.00 a box, and he spends $3.00 on cheddar cheese 
    and twice that amount for the gruyere cheese. Bud 
    spends 520 dollars on making macaroni and cheese in 
    x year. What is the value of unknown variable x?"},
    {"role":"assistant","content":"1"}
    ]
}
```

2. **Fine tuning approach**: We fine tuned the gpt 3.5 model through the official OpenAI fine-tuning tutorial by calling ```client.fine_tuning.jobs.create``` method.

#### 3. Naive Approach - base model of gpt 3.5-Turbo using COT & without using COT
Directly put the reverse math problem into the prompt and let the model generate the answer. The default base model uses COT. For the model without, use the follwing prompt:
```
{
      messages=[
      {"role": "system", "content": "\n You are a clever  
       mathematician. \n Please give me the answer of 
       the given questions. \n "},
      {"role": "user", "content": user_input},
      {"role": "user", "content": "Just give me the 
      answer."}  # Adding the follow-up request
    ]
}
```