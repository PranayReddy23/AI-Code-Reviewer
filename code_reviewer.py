import streamlit as st
import google.generativeai as genai
import re

# Helper function to escape special markdown characters, but only for human input
def escape_markdown(text, is_human_input=True):
    if not is_human_input:
        return text  # Do not escape for AI response (to preserve formatting)

    # If the message is code (starts and ends with triple backticks), do not escape it
    if text.startswith('```') and text.endswith('```'):
        return text  # Don't escape code blocks
    
    # Escape characters like '#', '*', '_', etc., that are used in markdown
    text = re.sub(r'([#*_`])', r'\\\1', text)
    return text

## Loading the Key
f = open('api_key.txt')
key = f.read()

## Configuring the Key
genai.configure(api_key=key)

## Initializing the model with system prompt
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=""" 
Application Purpose: 
You are an AI code reviewer designed to help users identify potential bugs, inefficiencies, and areas of improvement in Python code.

Target Audience: 
Programmers of all levels, from beginners seeking guidance on debugging to experienced developers looking for a second pair of eyes for optimization and best practices.

Key Features:
- Analyze Python code for syntax errors, logical bugs, and inefficiencies.
- Provide actionable suggestions for improvement and fixes, with clear code snippets.
- Maintain readability and alignment with Python best practices (PEP 8).
- Adapt explanations based on the user's expertise (e.g., detailed for beginners, concise for experts).

Desired Tone and Style:
Friendly, professional, and supportive. Keep responses engaging and non-judgmental to encourage users of all skill levels to seek help. Use simple language for clarity but avoid oversimplifying for advanced users.
"""
)

chatbot = model.start_chat(history=[])

## Setting the title
st.title("AI CODE REVIEWER")
st.chat_message("ai").write("Hello and welcome! 👋 I'm your AI-powered Python Code Reviewer, here to help you spot bugs, improve efficiency, and optimize your code. Feel free to share your Python code, and I'll provide suggestions to help you write better, cleaner code. Let's get started!")


## Using Session State to Store Chat History
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

## Displaying Previous Messages with Markdown Escaping Only for Human Input
for message in st.session_state.chat_history:
    escaped_message = escape_markdown(message['text'], is_human_input=(message['role'] == 'human'))
    if message['role'] == 'ai':
        st.chat_message('ai').write(escaped_message)
    else:
        st.chat_message('human').write(escaped_message)

## Taking prompts from the user
human_prompt = st.chat_input("Enter your Python code to review...")

if human_prompt:
    st.session_state.chat_history.append({'role': 'human', 'text': human_prompt})
    with st.spinner("AI is reviewing your code..."):
        response = chatbot.send_message(human_prompt)
    st.session_state.chat_history.append({'role': 'ai', 'text': response.text})

    # Escape markdown characters for human input, but not for AI response
    st.chat_message('human').write(escape_markdown(human_prompt, is_human_input=True))
    st.chat_message('ai').write(response.text)  # No need to escape for AI response
