import openai
import streamlit as st
import pandas as pd
from io import BytesIO

# Sidebar for OpenAI API key
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

openai.api_key = openai_api_key

# Functions
def generate_kanbun(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an expert in writing Kanbun (漢文) poems."},
        {"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def translate_kanbun_to_english(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in translating Kanbun (漢文) into English."},
                  {"role": "user", "content": f"Translate this Kanbun into English: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def extract_vocabulary(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in extracting vocabulary from Kanbun (漢文)."},
                  {"role": "user", "content": f"Extract interesting vocabulary from this Kanbun: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Main app logic
def main():
    st.title("AI Kanbun (漢文) Poem Generator")
    theme = st.text_input("Enter a theme for the poem (e.g., nature, seasons, flowers):")

    if st.button("Generate Kanbun"):
        if theme:
            prompt = f"Write a Kanbun (漢文) poem about {theme}."
            kanbun = generate_kanbun(prompt)
            translation = translate_kanbun_to_english(kanbun)
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("Generated Kanbun:")
            st.write(kanbun)

            st.subheader("English Translation:")
            st.write(translation)

            st.subheader("Interesting Vocabulary:")
            st.write(vocabulary)

            data = {
                "Theme": [theme],
                "Kanbun": [kanbun],
                "Translation": [translation],
                "Vocabulary": [vocabulary]
            }
            df = pd.DataFrame(data)

            st.subheader("Data Table:")
            st.dataframe(df)

            # CSV download
            st.download_button(
                label="Download as CSV",
                data=df.to_csv(index=False),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            # Excel download
            excel_data = BytesIO()
            df.to_excel(excel_data, index=False, engine='openpyxl')
            excel_data.seek(0)
            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Please provide a theme for the poem.")


if __name__ == "__main__":
    main()


