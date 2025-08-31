import streamlit as st
import pandas as pd
from difflib import get_close_matches

# Load FAQs
faqs = pd.read_csv("faqs.csv")

# Function to get best answer
def get_answer(user_question):
    questions = faqs['Question'].tolist()
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    if matches:
        match = matches[0]
        answer = faqs.loc[faqs['Question'] == match, 'Answer'].values[0]
        return answer, match
    else:
        return None, None

# --- Streamlit App ---
st.set_page_config(page_title="Student Support Chatbot", page_icon="🎓", layout="centered")

st.title("🎓 Student Support Chatbot")
st.write("Ask me anything about admission, exams, hostel, fees, scholarships, placements and more.")

# Session state for chatbot + feedback
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_match" not in st.session_state:
    st.session_state.last_match = None
if "feedback_msg" not in st.session_state:
    st.session_state.feedback_msg = None

# User input
user_question = st.text_input("💬 Type your question here:")

if st.button("Ask"):
    if user_question.strip():
        answer, match = get_answer(user_question)
        if answer:
            st.session_state.last_answer = answer
            st.session_state.last_match = match
        else:
            st.session_state.last_answer = "❌ Sorry, I don't have an answer for that yet. Try rephrasing your question."
            st.session_state.last_match = None
        st.session_state.feedback_msg = None   # reset feedback each time a new question is asked

# Show chatbot response
if st.session_state.last_answer:
    st.markdown(f"✅ **Answer:** {st.session_state.last_answer}")
    if st.session_state.last_match:
        st.markdown(f"💡 *You may have meant:* **{st.session_state.last_match}**")

    # Feedback Section
    st.markdown("### 📝 Was this answer helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Yes"):
            st.session_state.feedback_msg = "Thanks for your feedback! "
    with col2:
        if st.button("👎 No"):
            st.session_state.feedback_msg = "Sorry this wasn't helpful. We'll improve it! "

# Display feedback message (outside the button block)
if st.session_state.feedback_msg:
    if "Thanks" in st.session_state.feedback_msg:
        st.success(st.session_state.feedback_msg)
    else:
        st.warning(st.session_state.feedback_msg)
