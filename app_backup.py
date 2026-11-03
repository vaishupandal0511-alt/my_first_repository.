import streamlit as st
import ollama

st.set_page_config(
    page_title="DermaGlow AI",
    page_icon="✨",
    layout="centered"
)

st.title("✨ DermaGlow AI")
st.subheader("Your Intelligent Skincare Assistant")

st.write(
    "Welcome! I'm your AI skincare companion. "
    "Ask me about skincare routines, acne, pigmentation "
    "and healthy skin habits."
)

st.divider()

st.header("Let's understand your skin!")

name = st.text_input("What is your name?")

skin_type = st.selectbox(
    "What is your skin type?",
    ["Select your skin type", "Dry", "Oily",
     "Combination", "Sensitive", "Normal", "Not sure"]
)

concern = st.selectbox(
    "What is your main skin concern?",
    ["Select your concern", "Acne", "Pigmentation",
     "Dark spots", "Dryness", "Dullness", "Other"]
)

if st.button("Start My Skincare Journey"):
    if name and skin_type != "Select your skin type" and concern != "Select your concern":

        st.session_state.name = name
        st.session_state.skin_type = skin_type
        st.session_state.concern = concern

        st.success(f"Welcome, {name}! 💗")

    else:
        st.warning("Please complete all the fields.")

if "name" in st.session_state:

    st.divider()
    st.header("💬 Chat with DermaGlow AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Ask me anything about skincare...")

    if user_message:
        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )

        with st.chat_message("user"):
            st.write(user_message)

        system_prompt = f"""
        You are DermaGlow AI, a friendly skincare education assistant.

        User name: {st.session_state.name}
        Skin type: {st.session_state.skin_type}
        Main concern: {st.session_state.concern}

        Give gentle, practical, evidence-informed skincare guidance.
        Explain ingredients in simple language.
        Avoid diagnosing diseases or prescribing medicines.
        Recommend a dermatologist for severe, persistent or painful
        skin problems. Never guarantee results.
        """

        with st.chat_message("assistant"):
            with st.spinner("DermaGlow AI is thinking..."):

                try:
                    response = ollama.chat(
                        model="llama3.2:1b",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.messages
                        ]
                    )

                    answer = response["message"]["content"]
                    st.write(answer)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as e:
                    st.error(f"Unable to connect to AI: {e}")

st.divider()

st.caption(
    "DermaGlow AI provides general skincare education, "
    "not medical diagnosis or treatment."
)