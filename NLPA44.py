import openai
import streamlit as st
import pandas as pd

# Add custom styling
st.markdown("""
    <style>
    body {
        background-color: #FFDDE6; /* Pastel pink background */
    }
    .stApp {
        background-color: #FFDDE6;
    }
    h1 {
        color: #FF69B4; /* Hot pink title color */
        font-family: 'Kaushan Script', cursive; /* Japanese-style font */
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px #FFB6C1; /* Soft pink shadow */
    }
    .stButton button {
        background-color: #FFB6C1; /* Light pink buttons */
        color: #8B0000; /* Deep red text */
        font-size: 16px;
        border-radius: 12px;
        border: 2px solid #FF69B4;
        font-family: 'Arial', sans-serif;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background-color: #FF9BB2; /* Slightly darker pink on hover */
    }
    .stTextInput textarea {
        background-color: #FFF0F5; /* Lavender blush input field */
        color: #8B0000; /* Deep red text */
        font-size: 14px;
        border: 2px solid #FF69B4;
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
        padding: 10px;
    }
    .stDataFrame {
        background-color: #FFF5F7; /* Light pink for DataFrame */
        border: 2px solid #FFC0CB; /* Pink border */
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #FFDDE6; /* Match the app background */
    }
    footer {
        font-family: 'Kaushan Script', cursive;
        text-align: center;
        padding: 10px;
        color: #FF69B4;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API key input
openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key:", type="password")
if openai_api_key:
    openai.api_key = openai_api_key

# Function to generate Kanbun
def generate_kanbun(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a skilled Kanbun (classical Chinese) poet."},
                  {"role": "user", "content": prompt}]
    )
    kanbun = response['choices'][0]['message']['content'].strip()
    return kanbun

# Function to translate Kanbun to English
def translate_kanbun_to_english(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in translating Kanbun (classical Chinese) into English."},
                  {"role": "user", "content": f"Translate this Kanbun into English: {kanbun}"}]
    )
    translation = response['choices'][0]['message']['content'].strip()
    return translation

# Function to extract vocabulary from Kanbun
def extract_vocabulary(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing Kanbun (Chinese texts with Japanese reading order) and providing translations with part-of-speech tagging."},
            {"role": "user", "content": f"Extract important vocabulary from the following Kanbun text (a Chinese poem with Japanese reading order) and provide the English translation along with part-of-speech tags (e.g., noun, verb, adjective, etc.):\n{kanbun}"}
        ]
    )
    vocabulary = response['choices'][0]['message']['content'].strip()
    return vocabulary

# Main application function
def main():
    st.title("\u2728 AI-Generated Kanbun Poetry \u2728")

    # Brief explanation about Kanbun
    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into English, and provides key vocabulary for further analysis.
    """)

    sentence = st.text_area("\uD83C\uDF38 Enter a sentence or passage for the Kanbun poem (e.g., a short story or a descriptive paragraph):")

    if st.button("\u2728 Generate Kanbun \u2728"):
        if sentence:
            prompt = f"Create a Kanbun (classical Chinese) poem based on the following sentence or passage: {sentence}"
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to English
            translation = translate_kanbun_to_english(kanbun)

            # Extract vocabulary
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("\uD83D\uDCDC Generated Kanbun Poem:")
            st.write(kanbun)

            st.subheader("\uD83C\uDF10 English Translation:")
            st.write(translation)

            st.subheader("\uD83D\uDCD3 Key Vocabulary from the Kanbun:")
            st.write(vocabulary)

            data = {
                "Input Sentence/Passage": [sentence],
                "Kanbun Poem": [kanbun],
                "English Translation": [translation],
                "Key Vocabulary": [vocabulary]
            }
            df = pd.DataFrame(data)

            # Display DataFrame
            st.subheader("\uD83D\uDCCA Poem Details in Table Format:")
            st.dataframe(df)

            # Download buttons for CSV and Excel
            st.download_button(
                label="\uD83D\uDCBE Download as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="\uD83D\uDCC4 Download as Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("\u26A0\uFE0F Please enter a sentence or passage to generate a poem \u26A0\uFE0F")

if __name__ == "__main__":
    main()
