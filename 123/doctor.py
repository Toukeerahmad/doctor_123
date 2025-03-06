import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure genai with API key
genai.configure(api_key=api_key)

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.4,
        
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
)

system_prompt = """
You are a helpful medical chatbot assisting users with health-related questions. 
Your Responsibilities include:
1. Providing information on medical topics.
2. Suggesting possible treatments based on symptoms.
3. Offering advice on when to seek professional medical care.
4. Recommending top 10 hospitals in Bangalore if requested.

Important Notes:
- Always include a disclaimer: "Consult with a Doctor before making any decisions."
- If the question is outside medical advice, politely refuse.
"""

# Set Streamlit page config
st.set_page_config(page_title="Medical Chatbot", page_icon=":robot:")
st.title("Medical Chatbot")
st.header("Ask your health-related questions!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate model response
    prompt_parts = [system_prompt, user_input]
    response = model.generate_content(prompt_parts)

    bot_response = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)