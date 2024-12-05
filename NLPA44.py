import openai
import streamlit as st
import pandas as pd

# Add custom styling
st.markdown("""
    <style>
    body {
        background-color: #F5F5F5; /* Light gray background */
    }
    .stApp {
        background-color: #F5F5F5;
    }
    h1 {
        color: #1E88E5; /* Blue title color */
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .stButton button {
        background-color: #81D4FA; /* Light blue buttons */
        color: #0D47A1; /* Dark blue text */
        font-size: 16px;
        border-radius: 12px;
        border: 2px solid #29B6F6;
    }
    .stButton button:hover {
        background-color: #4FC3F7; /* Slightly darker blue on hover */
    }
    .stTextInput input {
        background-color: #E3F2FD; /* Light blue input field */
        color: #0D47A1; /* Dark blue text */
        font-size: 14px;
        border: 2px solid #64B5F6;
        border-radius: 10px;
    }
    .stDataFrame {
        background-color: #E8F5E9; /* Light green for DataFrame */
        border: 2px solid #A5D6A7; /* Green border */
        border-radius: 10px;
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
                  {"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    kanbun = response.choices[0].message['content'].strip()
    return kanbun

# Function to translate Kanbun to English
def translate_kanbun_to_english(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in translating Kanbun (classical Chinese) into English."},
                  {"role": "user", "content": f"Translate this Kanbun into English: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    translation = response.choices[0].message['content'].strip()
    return translation

# Function to extract vocabulary from Kanbun
def extract_vocabulary(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing Kanbun (Chinese texts with Japanese reading order) and providing translations with part-of-speech tagging."},
            {"role": "user", "content": f"Extract important vocabulary from the following Kanbun text (a Chinese poem with Japanese reading order) and provide the English translation along with part-of-speech tags (e.g., noun, verb, adjective, etc.):\n{kanbun}"}
        ],
        max_tokens=500,
        temperature=0.7
    )
    vocabulary = response.choices[0].message['content'].strip()
    return vocabulary

# Main application function
def main():
    st.title("🌸 AI-Generated Kanbun Poetry 🌸")

    # Brief explanation about Kanbun
    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into English, and provides key vocabulary for further analysis.
    """)

    sentence = st.text_area("🌼 Enter a sentence or passage for the Kanbun poem (e.g., a short story or a descriptive paragraph):")

    if st.button("✨ Generate Kanbun ✨"):
        if sentence:
            prompt = f"Create a Kanbun (classical Chinese) poem based on the following sentence or passage: {sentence}"
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to English
            translation = translate_kanbun_to_english(kanbun)

            # Extract vocabulary
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("📜 Generated Kanbun Poem:")
            st.write(kanbun)

            st.subheader("🌐 English Translation:")
            st.write(translation)

            st.subheader("📚 Key Vocabulary from the Kanbun:")
            st.write(vocabulary)

            data = {
                "Input Sentence/Passage": [sentence],
                "Kanbun Poem": [kanbun],
                "English Translation": [translation],
                "Key Vocabulary": [vocabulary]
            }
            df = pd.DataFrame(data)

            # Display DataFrame
            st.subheader("📊 Poem Details in Table Format:")
            st.dataframe(df)

            # Download buttons for CSV and Excel
            st.download_button(
                label="💾 Download as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="📄 Download as Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ Please enter a sentence or passage to generate a poem ⚠️")

if __name__ == "__main__":
    main()
