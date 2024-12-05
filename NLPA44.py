import openai
import streamlit as st
import pandas as pd

# Configure the OpenAI API key
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if openai_api_key:
    openai.api_key = openai_api_key

# Function to generate Kanbun (漢文) poems using the OpenAI API
def generate_kanbun(prompt):
    # Send a request to ChatGPT to create a poem
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you want to use GPT-4
        messages=[{"role": "system", "content": "You are an expert in writing Kanbun (漢文) poems."},
                  {"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    kanbun = response.choices[0].message.content.strip()
    return kanbun

# Function to translate Kanbun (漢文) into English
def translate_kanbun_to_english(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in translating Kanbun (漢文) into English."},
                  {"role": "user", "content": f"Translate this Kanbun into English: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    translation = response.choices[0].message.content.strip()
    return translation

# Function to extract interesting vocabulary from Kanbun (漢文)
def extract_vocabulary(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in extracting vocabulary from Kanbun (漢文)."},
                  {"role": "user", "content": f"Extract interesting vocabulary from this Kanbun: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    vocabulary = response.choices[0].message.content.strip()
    return vocabulary

# Main function to handle the Streamlit app
def main():
    st.title("AI Kanbun (漢文) Poem Generator")

    theme = st.text_input("Enter a theme for the poem (e.g., nature, seasons, flowers):")

    if st.button("Generate Kanbun"):
        if theme:
            prompt = f"Create a Kanbun (漢文) poem related to {theme}."
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to English
            translation = translate_kanbun_to_english(kanbun)

            # Extract interesting vocabulary
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("Generated Kanbun Poem:")
            st.write(kanbun)

            st.subheader("English Translation:")
            st.write(translation)

            st.subheader("Interesting Vocabulary from Kanbun:")
            st.write(vocabulary)

            data = {
                "Theme": [theme],
                "Kanbun Poem": [kanbun],
                "English Translation": [translation],
                "Interesting Vocabulary": [vocabulary]
            }
            df = pd.DataFrame(data)

            # Display DataFrame
            st.subheader("Data in Table Format:")
            st.dataframe(df)

            # CSV download button
            st.download_button(
                label="Download as CSV",
                data=df.to_csv(index=False),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            # Excel download button
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
