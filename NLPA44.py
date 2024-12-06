import openai
import streamlit as st
import pandas as pd
import random

# Add custom styling with seasonal visuals
st.markdown("""
    <style>
    /* Seasonal Background */
    body {
        background-image: url('https://example.com/cherry_blossom.jpg');
        background-size: cover;
        color: #4D4D4D;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 10px;
    }
    h1 {
        color: #FFB3BA;
        font-family: 'Arial', sans-serif;
        text-align: center;
        animation: fadeIn 3s;
    }
    .stButton button {
        background-color: #FFDFD3;
        color: #D47F6A;
        font-size: 16px;
        border-radius: 12px;
        border: 2px solid #FFB3BA;
    }
    .stButton button:hover {
        background-color: #FFD1C1;
    }
    /* Keyframe for fade-in effect */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for settings and mode toggle
st.sidebar.title("Settings")
openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key:", type="password")
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

if openai_api_key:
    openai.api_key = openai_api_key

# Function to generate Kanbun
def generate_kanbun(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a skilled Kanbun (classical Chinese) poet."},
            {"role": "user", "content": prompt}
        ]
    )
    kanbun = response['choices'][0]['message']['content'].strip()
    return kanbun

# Function to translate Kanbun to a selected language
def translate_kanbun(kanbun, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in translating Kanbun (classical Chinese) into {target_language}."},
            {"role": "user", "content": f"Translate this Kanbun into {target_language}: {kanbun}"}
        ]
    )
    translation = response['choices'][0]['message']['content'].strip()
    return translation

# Function to extract vocabulary with extra details
def extract_vocabulary(kanbun, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in analyzing Kanbun (Chinese texts with Japanese reading order) and providing translations with part-of-speech tagging, JLPT levels, and example sentences in {target_language}."},
            {"role": "user", "content": f"Extract important vocabulary from the following Kanbun text and provide {target_language} translation, romaji pronunciation, JLPT levels, part-of-speech tags, and example sentences:\n{kanbun}"}
        ]
    )
    vocabulary = response['choices'][0]['message']['content'].strip()
    return vocabulary

# Flashcard generator for vocabulary practice
def generate_flashcard(vocab):
    word, romaji, meaning = random.choice(vocab)
    st.write(f"### Word: {word} ({romaji})")
    if st.button("Show Meaning"):
        st.write(f"### Meaning: {meaning}")

# Main application function
def main():
    st.title("🌸 Learn Japanese with Kanbun Poetry 🌸")

    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into a selected language, and provides tools for further analysis and learning.
    """)

    sentence = st.text_area("🌸 Enter a sentence or passage for the Kanbun poem:")

    # Language selection for translation
    languages = ["English", "Thai", "Korean", "French", "Spanish", "German", "Italian", "Portuguese", "Arabic", "Icelandic", "Swahili", "Finnish", "Greek", "Hindi", "Malay", "Turkish", "Vietnamese", "Russian", "Dutch", "Hebrew"]
    target_language = st.selectbox("🌐 Select the language for translation:", languages)

    if st.button("✨ Generate Kanbun ✨"):
        if sentence:
            prompt = f"Create a Kanbun (classical Chinese) poem based on the following sentence or passage: {sentence}"
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to the selected language
            translation = translate_kanbun(kanbun, target_language)

            # Extract vocabulary with added details
            vocabulary = extract_vocabulary(kanbun, target_language)

            st.subheader("🕌 Generated Kanbun Poem:")
            st.write(kanbun)

            st.subheader(f"🌐 Translation to {target_language}:")
            st.write(translation)

            st.subheader(f"📚 Vocabulary with Details:")
            st.write(vocabulary)

            # Flashcard Practice Section
            st.subheader("Flashcard Practice")
            st.markdown("Test your memory and learn vocabulary interactively!")
            generate_flashcard(vocabulary)

            # Grammar Insights Placeholder
            st.subheader("Grammar Insights")
            st.markdown("Detailed grammar breakdown for each line will appear here.")

            # Cultural Context Placeholder
            st.subheader("Cultural Context")
            st.markdown("Relevant cultural and historical insights will appear here.")

if __name__ == "__main__":
    main()
