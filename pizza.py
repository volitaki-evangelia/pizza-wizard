import streamlit as st
import google.generativeai as genai
import os

# Ρύθμιση της σελίδας
st.set_page_config(page_title="The Great Pizza Rescue", page_icon="🍕", layout="centered")

# Custom CSS για παιδικό στυλ
st.markdown("""
    <style>
    .stApp { background-color: #FFFDF0; }
    h1 { color: #FF5733; font-family: 'Comic Sans MS', cursive, sans-serif; text-align: center; font-size: 42px !important; text-shadow: 2px 2px #FFC300; }
    h3 { color: #C70039; font-family: 'Comic Sans MS', sans-serif; text-align: center; font-size: 24px !important; }
    .wizard-box { background-color: #E8F8F5; border-left: 8px solid #1ABC9C; border-radius: 15px; padding: 20px; font-size: 20px !important; font-family: 'Comic Sans MS', sans-serif; color: #1A5235; }
    .class-box { background-color: #FEF9E7; border-left: 8px solid #F1C40F; border-radius: 15px; padding: 15px; font-size: 18px !important; font-family: 'Comic Sans MS', sans-serif; margin-top: 10px; color: #7D6608; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🍕 THE GREAT PIZZA RESCUE 🍕</h1>", unsafe_allow_html=True)
st.markdown("<h3>✨ STEM & Fractions Magic Game! ✨</h3>", unsafe_allow_html=True)
st.markdown("---")

# Ανάκτηση API Key από τα Secrets
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if not api_key:
    st.error("⚠️ Configuration Error! Please check your GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Ρύθμιση του AI Μοντέλου
genai.configure(api_key=api_key)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
model = genai.GenerativeModel('gemini-2.5-flash', safety_settings=safety_settings)

# Αρχικοποίηση παιχνιδιού
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    system_prompt = (
        "Act as the 'Fraction Wizard' (a friendly, extremely enthusiastic, and playful math teacher wizard) "
        "in an interactive story-game for 8-10 year old school kids. The game is called 'The Great Pizza Rescue'. "
        "You will give the class 3 simple, fun puzzles about math fractions using a pizza pie as a clear example. "
        "Level 1: Halves (1/2). Level 2: Quarters (1/4 or 3/4). Level 3: A question about equal vs unequal parts. "
        "Rules: 1. Use lots of emojis (🍕, 🧙‍♂️, ✨) and clear, encouraging English suitable for elementary school pupils. "
        "2. Start IMMEDIATELY by introducing yourself with a nice magical welcome and giving ONLY Level 1. Then STOP and wait for their reply. "
        "3. If they are correct, congratulate them warmly and unlock the next level. "
        "4. If they give an incorrect answer, encourage them, give a gentle hint, and ask them to try again."
    )
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(system_prompt)
        st.session_state.chat_history.append({"role": "wizard", "text": response.text})
    except Exception as e:
        st.error("🧙‍♂️ The Wizard is charging his magic wand! Please refresh the page in 10 seconds. ✨")
        st.stop()

# Εμφάνιση της συνομιλίας
for message in st.session_state.chat_history:
    if message["role"] == "wizard":
        st.markdown(f"<div class='wizard-box'>🧙‍♂️ <b>Fraction Wizard:</b><br>{message['text']}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='class-box'>👦👧 <b>Our Class:</b> {message['text']}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# 🔊 ΑΥΤΟΜΑΤΗ ΦΩΝΗ: Παίρνει το τελευταίο μήνυμα του Μάγου και το διαβάζει αυτόματα με το που φορτώνει η σελίδα!
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "wizard":
    last_text = st.session_state.chat_history[-1]["text"]
    clean_text = ''.join(c for c in last_text if c.isalnum() or c.isspace() or c in ['.', ',', '?', '!'])
    clean_text = clean_text.replace("'", "").replace('"', "")
    
    # Εισαγωγή ασφαλούς script που εκτελείται απευθείας στην κεντρική σελίδα
    st.components.v1.html(f"""
        <script>
            window.parent.speechSynthesis.cancel();
            var speech = new window.parent.SpeechSynthesisUtterance("{clean_text}");
            speech.lang = 'en-US';
            speech.rate = 0.85;
            speech.pitch = 1.1;
            window.parent.speechSynthesis.speak(speech);
        </script>
    """, height=0, width=0)

st.markdown("---")

# Φόρμα απάντησης
with st.form(key="pizza_form", clear_on_submit=True):
    st.markdown("### 📝 Enter your Magical Answer here:")
    user_input = st.text_input("", placeholder="Type your answer to the Wizard...", key="user_ans")
    submit_button = st.form_submit_button(label="🚀 Cast the Math Spell!")

if submit_button and user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    chat_history_formatted = []
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "model"
        chat_history_formatted.append({"role": role, "parts": [msg["text"]]})
    
    with st.spinner("🧙‍♂️ The Wizard is waving his magic wand... ✨"):
        try:
            chat = model.start_chat(history=chat_history_formatted[:-1])
            response = chat.send_message(user_input)
            st.session_state.chat_history.append({"role": "wizard", "text": response.text})
        except Exception as e:
            st.warning("🔮 Magic limit reached! The Wizard is resting for 5 seconds. Please re-submit your answer now!")
            st.session_state.chat_history.pop()
            st.stop()
    
    if any(word in response.text.lower() for word in ["correct", "next level", "win", "🎉", "awesome", "perfect"]):
        st.balloons()
        
    st.rerun()

# Κουμπί επανεκκίνησης
if st.button("🔄 Restart Magic Mission"):
    st.session_state.clear()
    st.rerun()
