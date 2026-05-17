import streamlit as st
import google.generativeai as genai
import os

# Page Configuration
st.set_page_config(page_title="The Great Pizza Rescue", page_icon="🍕", layout="centered")

# Title and Introduction
st.title("🍕 The Great Pizza Rescue: STEM & Fractions")
st.subheader("Lesson: Introduction to Fractions (Grades 3–4)")
st.markdown("---")

# Retrieve the API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    st.error("⚠️ Please configure the GEMINI_API_KEY in your Streamlit Secrets for the AI to work.")
    st.stop()

# Configure the AI Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize Session State (Game Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Hidden system prompt to guide the AI behavior in English
    system_prompt = (
        "Act as the 'Fraction Wizard' (a friendly, enthusiastic, and playful fairytale wizard) "
        "in an interactive game for 8-10 year old students (3rd-4th Grade). The game is called 'The Great Pizza Rescue'. "
        "You will give the class 3 sequential riddles about introductory fractions based on sharing a pizza fairly. "
        "Level 1 must focus on halves (1/2). Level 2 must focus on quarters (1/4 or 3/4). Level 3 must test critical thinking about unequal parts. "
        "Rules: 1. Speak exclusively in English with an engaging, magical tone. "
        "2. Start IMMEDIATELY by welcoming them and giving ONLY the first riddle (Level 1), then STOP and wait for their answer. "
        "3. If they answer correctly, celebrate enthusiastically and move to the next Level. "
        "4. If they give a wrong answer, do not give away the solution! Provide a fun, simple mathematical hint and ask them to try again."
    )
    # Start the conversation
    chat = model.start_chat(history=[])
    response = chat.send_message(system_prompt)
    st.session_state.chat_history.append({"role": "wizard", "text": response.text})

# Display the ongoing Chat History
for message in st.session_state.chat_history:
    if message["role"] == "wizard":
        st.info(f"🧙‍♂️ **Fraction Wizard:** {message['text']}")
    else:
        st.success(f"👦👧 **Class:** {message['text']}")

# Input form for students
st.markdown("### 📝 The Classroom's Answer:")
with st.form(key="pizza_form", clear_on_submit=True):
    user_input = st.text_input("Type your answer or ask the Wizard a question:", key="user_ans")
    submit_button = st.form_submit_button(label="🚀 Send to the Wizard!")

if submit_button and user_input:
    # Append classroom answer to history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    # Format the history for the Gemini API
    chat_history_formatted = []
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "model"
        chat_history_formatted.append({"role": role, "parts": [msg["text"]]})
    
    # Send message to AI and fetch response
    with st.spinner("🧙‍♂️ The Wizard is thinking..."):
        chat = model.start_chat(history=chat_history_formatted[:-1])
        response = chat.send_message(user_input)
        st.session_state.chat_history.append({"role": "wizard", "text": response.text})
    
    # Rerun the app to show updates
    st.rerun()

# Reset Game Button
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()
