import streamlit as st
import ollama

st.set_page_config(
    page_title="DermaGlow AI",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #FFF8F6;
}
h1, h2, h3 {
    color: #9C5969;
}
p, label {
    color: #55434A;
}
.stButton > button {
    background-color: #C77D91;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 22px;
}
.stButton > button:hover {
    background-color: #A95E75;
    color: white;
}
[data-testid="stChatMessage"] {
    background-color: #FFF0F1;
    border-radius: 14px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ DermaGlow AI")
st.subheader("Your Intelligent Skincare Assistant")

st.markdown(
    "Welcome to your personal skincare space. "
    "Understand your skin, explore gentle routines "
    "and discover helpful skincare ingredients."
)

st.divider()

with st.sidebar:
    st.header("🌸 Your Skin Profile")

    name = st.text_input("Your name")

    skin_type = st.selectbox(
        "Select your skin type",
        ["Not selected", "Dry", "Oily", "Combination",
         "Sensitive", "Normal", "Not sure"]
    )

    concern = st.selectbox(
        "Main skin concern",
        ["Not selected", "Acne", "Pigmentation",
         "Dark spots", "Dryness", "Dullness", "Other"]
    )

    if st.button("Save My Skin Profile"):
        if name and skin_type != "Not selected" and concern != "Not selected":
            st.session_state.profile = {
                "name": name,
                "skin_type": skin_type,
                "concern": concern
            }
            st.success("Your skin profile is saved!")
        else:
            st.warning("Please complete all fields.")

if "profile" not in st.session_state:
    st.info("👈 Start by entering your skin details in the sidebar.")
else:
    profile = st.session_state.profile

    st.success(
        f"Welcome, {profile['name']}! "
        f"Your profile is ready. 💗"
    )

    st.markdown("### 🌷 Your Skincare Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input(
        "Ask me about acne, pigmentation, routines or ingredients..."
    )

    if user_message:
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        system_prompt = f"""
        You are DermaGlow AI, a friendly skincare education assistant.

        User name: {profile['name']}
        Skin type: {profile['skin_type']}
        Main concern: {profile['concern']}

        Give clear, gentle, evidence-informed skincare guidance.
        Explain ingredients in simple language.
        Suggest simple morning and evening routines when relevant.
        Consider the user's skin type and concern.
        Do not diagnose diseases or prescribe medicines.
        Do not guarantee results.
        Recommend a dermatologist for severe or persistent problems.
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

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as error:
                    st.error(f"AI connection error: {error}")

st.divider()

st.caption(
    "DermaGlow AI | General skincare education, "
    "not a substitute for professional medical advice."
)
st.subheader("🧪 Skincare Ingredient Checker")

ingredient = st.text_input(
    "Enter a skincare ingredient",
    placeholder="e.g., Niacinamide"
)

if st.button("Check Ingredient"):
    if ingredient.strip():
        with st.spinner("DermaGlow AI is checking the ingredient..."):
            try:
                result = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cautious skincare education assistant. "
                                "Explain ingredients in simple language. "
                                "Cover benefits, suitable skin types, cautious usage, "
                                "and possible irritation. Mention patch testing. "
                                "Do not diagnose or prescribe treatments."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Explain {ingredient}: what it does, who may benefit, "
                                "how to use it cautiously, and possible side effects."
                            )
                        }
                    ]
                )

                st.write(result["message"]["content"])

            except Exception as error:
                st.error(f"AI connection error: {error}")
    else:
        st.warning("Please enter an ingredient.")
        st.subheader("🧴 Product Recommendation Assistant")

product_skin = st.selectbox(
    "Choose your skin type",
    ["Dry", "Oily", "Combination", "Sensitive", "Normal"],
    key="product_skin"
)

product_concern = st.selectbox(
    "Choose your main skin concern",
    ["Acne", "Pigmentation", "Dark spots",
     "Dryness", "Dullness", "Sensitive skin"],
    key="product_concern"
)

if st.button("Recommend Skincare Products"):
    with st.spinner("Finding suitable skincare options..."):
        try:
            result = ollama.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cautious skincare education assistant. "
                            "Suggest suitable product types and helpful ingredients, "
                            "not fabricated brand names or products. "
                            "Explain why each suggestion may help. "
                            "Mention patch testing and possible irritation. "
                            "Do not diagnose or prescribe medicines."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Suggest a simple skincare routine for "
                            f"{product_skin} skin with {product_concern}. "
                            "Include suitable product types, ingredients "
                            "to look for, and precautions."
                        )
                    }
                ]
            )

            st.markdown(result["message"]["content"])

        except Exception as error:
            st.error(f"AI connection error: {error}")
            st.subheader("🌞 Daily Skincare Routine Generator")

routine_skin = st.selectbox(
    "Select your skin type",
    ["Dry", "Oily", "Combination", "Sensitive", "Normal"],
    key="routine_skin"
)

routine_concern = st.selectbox(
    "Select your skin concern",
    ["Acne", "Pigmentation", "Dark spots",
     "Dryness", "Dullness", "Sensitive skin"],
    key="routine_concern"
)

if st.button("Generate My Daily Routine"):
    with st.spinner("Creating your personalized routine..."):
        try:
            result = ollama.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cautious skincare education assistant. "
                            "Create a simple morning and evening skincare routine. "
                            "Include cleanser, moisturizer and sunscreen where appropriate. "
                            "Explain how to introduce active ingredients slowly. "
                            "Mention patch testing and possible irritation. "
                            "Do not diagnose or prescribe medicines."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create a daily skincare routine for "
                            f"{routine_skin} skin with {routine_concern}. "
                            "Separate it into morning and evening steps."
                        )
                    }
                ]
            )

            st.markdown(result["message"]["content"])

        except Exception as error:
            st.error(f"AI connection error: {error}")
st.subheader("🌸 Skincare Quiz")

st.write("Answer these questions to receive personalized skincare guidance.")

quiz_skin = st.selectbox(
    "1. How does your skin usually feel after washing?",
    ["Tight or dry", "Oily", "Comfortable", "Both oily and dry"],
    key="quiz_skin"
)

quiz_sensitivity = st.radio(
    "2. Does your skin react easily to skincare products?",
    ["Yes", "No", "Sometimes"],
    key="quiz_sensitivity"
)

quiz_habit = st.radio(
    "3. Do you use sunscreen regularly?",
    ["Every day", "Sometimes", "Never"],
    key="quiz_habit"
)

quiz_concern = st.selectbox(
    "4. What is your biggest skincare concern?",
    ["Acne", "Pigmentation", "Dark spots",
     "Dryness", "Dullness", "No major concern"],
    key="quiz_concern"
)

if st.button("Get My Skincare Quiz Results"):
    with st.spinner("Analyzing your answers..."):
        try:
            result = ollama.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cautious skincare education assistant. "
                            "Summarize the user's answers and give simple, "
                            "general skincare guidance. Do not diagnose skin "
                            "conditions or prescribe medicines. Explain that "
                            "a short quiz cannot determine an exact skin type."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"After washing: {quiz_skin}. "
                            f"Skin sensitivity: {quiz_sensitivity}. "
                            f"Sunscreen habit: {quiz_habit}. "
                            f"Main concern: {quiz_concern}. "
                            "Give me a short summary and helpful skincare tips."
                        )
                    }
                ]
            )

            st.markdown("### 💗 Your Quiz Results")
            st.write(result["message"]["content"])

        except Exception as error:
            st.error(f"AI connection error: {error}")
            st.subheader("💾 Save My Skincare Routine")

routine_to_save = st.text_area(
    "Paste your generated skincare routine here",
    placeholder="Paste your morning and evening routine here..."
)

if st.button("Save My Routine"):
    if routine_to_save.strip():
        st.session_state.saved_routine = routine_to_save
        st.success("Your skincare routine has been saved! 💗")
    else:
        st.warning("Please enter your routine before saving.")

if "saved_routine" in st.session_state:
    st.markdown("### 🌸 Your Saved Routine")
    st.write(st.session_state.saved_routine)
st.divider()
st.subheader("⚠️ Skin Safety Checker")

safety_item = st.text_input(
    "Enter an ingredient or skincare product",
    placeholder="e.g., Retinol or Salicylic Acid",
    key="safety_item"
)

if st.button("Check Skin Safety"):
    if safety_item.strip():
        with st.spinner("Checking possible precautions..."):
            try:
                result = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cautious skincare education assistant. "
                                "Explain general safety considerations, possible "
                                "irritation, who should seek professional advice, "
                                "and patch testing. Safety depends on concentration, "
                                "formulation and individual sensitivity. "
                                "Never declare a product completely safe or unsafe. "
                                "Do not diagnose or prescribe."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Explain the skincare safety precautions for "
                                f"{safety_item} in simple language."
                            )
                        }
                    ]
                )

                st.markdown(result["message"]["content"])

            except Exception as error:
                st.error(f"AI connection error: {error}")
    else:
        st.warning("Please enter an ingredient or product name.")
st.caption(
    "DermaGlow AI | General skincare education, "
    "not a substitute for professional medical advice."
)