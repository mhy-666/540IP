import streamlit as st
from openai import OpenAI

def ft_response(user_input):

    response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::9CBKKv54",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input}
    ]
    )
    return response.choices[0].message.content

def direct_response(user_input):
    user_input = user_input + " Just give me the answer."

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input},
      {"role": "user", "content": "Just give me the answer."}  # Adding the follow-up request
    ]
    )
    return response.choices[0].message.content

def response(user_input):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input}
    ]
    )
    return response.choices[0].message.content



def main():


    st.title("Reverse Math Solver")

    # Initialize the conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    user_input = st.text_input("Enter your query:", "")

    # Generate a response using the backend function
    if user_input and st.button("Submit"):
        st.markdown(user_input)
        st.markdown("**Response using reverse solver:**")
        st.write(ft_response(user_input))
        st.markdown("**Response using gpt 3.5 turbo:**")
        st.write(direct_response(user_input))
        st.markdown("**Response using gpt 3.5 turbo with chain of thought:**")
        st.write(response(user_input))

if __name__ == "__main__":
    client = OpenAI(api_key = st.secrets['open_ai_key'])
    main()
