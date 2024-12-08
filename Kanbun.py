import openai
import streamlit as st
import pandas as pd
import openpyxl as xl
import io
from io import BytesIO

generate_button = st.markdown(
    """
    <style>
    .stButton button {
        background-color: transparent; /* Transparent background */
        color: #D47F6A; /* Soft peach text */
        font-size: 16px;
        border-radius: 12px;
        border: 2px solid #FFB3BA; /* Light pastel border */ 
        cursor: pointer; /* Pointer cursor for better UX */
    }
    .stButton button:hover {
        background-color: #FFD1C1; /* Slightly darker pastel coral on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

api_key = st.sidebar.text_input("🔑 Enter your OpenAI API key:", type="password")
key_provided = bool(api_key)  # Check if the key is provided

def generate_kanbun(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a skilled Kanbun (Japanese method of reading, annotating, and translating literary Chinese) poet."},
            {"role": "user", "content": prompt}
        ]
    )
    kanbun = response.choices[0].message.content.strip()
    return kanbun

def convert_kanbun_to_japanese(kanbun):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in converting Kanbun (Japanese method of reading, annotating, and translating literary Chinese) into modern Japanese."},
            {"role": "user", "content": f"Convert this Kanbun text to Japanese:\n{kanbun}"}
        ]
    )
    japanese = response.choices[0].message.content.strip()
    return japanese

def translate_kanbun(japanese_text, target_language):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in translating Japanese text into {target_language}."},
            {"role": "user", "content": f"Translate this Japanese text into {target_language}:\n{japanese_text}"}
        ]
    )
    translation = response.choices[0].message.content.strip()
    return translation

def extract_vocabulary(translation, target_language):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in analyzing Japanese text and providing translations with part-of-speech tagging, JLPT levels, and pronunciation in {target_language}."},
            {"role": "user", "content": f"Extract important Japanese vocabulary from the following Kanbun text and provide the {target_language} translation, romaji (pronunciation), example sentences of those Japanese words, part-of-speech tags (e.g., noun, verb, adjective, etc.), and JLPT levels sorted from N5 to N1:\n{translation}, do not say intro, just give me the lists"}
        ]
    )
    vocabulary = response.choices[0].message.content.strip()
    return vocabulary

def main():
    st.markdown(
    """
    <h1 style="text-align: center; font-size: 2.5em;">
        🌸 Learn Japanese with <span style="border-bottom: 3px solid #FFB3BA;">Kanbun Poetry</span> 🌸
    </h1>
    """,
    unsafe_allow_html=True
    )

    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into a selected language, and provides key vocabulary for further analysis!
    """)

    st.markdown("""
    **📜 Examples of Kanbun:** 
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("https://i.pinimg.com/736x/cf/8a/dd/cf8add09fa8261f23fcae8347a181fe5.jpg", width=350)

    with col2:
        st.image("https://media.eboard.jp/media/quiz_images/kanbun1_01_20220303.jpg", width=350)

    starter_text = "The cherry blossoms bloom as the sun rises, painting the sky with hues of pink and gold."
    sentence = st.text_area("**🌻 Enter a sentence or passage for the Kanbun poem (e.g., a short story or a descriptive paragraph):**", value=starter_text)

    languages = [
        "English", "Thai", "Korean", "French", "Spanish", "German", "Italian", "Portuguese", "Chinese (Simplified)",
        "Arabic", "Russian", "Hindi", "Bengali", "Vietnamese", "Turkish", "Indonesian", "Malay", "Swahili", "Dutch", "Greek"
    ]
    target_language = st.selectbox("**🌐 Select the language for translation:**", languages)

    generate_clicked = st.button("✨ Generate Kanbun ✨")

    if generate_clicked:
        if not key_provided:
            # Show the warning below the button
            st.warning("⚠️ Please enter a valid API key ⚠️")
        elif sentence:
            try:
                openai.api_key = api_key
                prompt = f"Create a Kanbun (Japanese method of reading, annotating, and translating literary Chinese) poem based on the following sentence or passage: {sentence}"
                kanbun = generate_kanbun(prompt)

                # Convert Kanbun to Japanese
                japanese_text = convert_kanbun_to_japanese(kanbun)

                # Translate Japanese to the target language
                translation = translate_kanbun(japanese_text, target_language)

                # Extract Vocabulary
                vocabulary = extract_vocabulary(kanbun, target_language)

                st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                st.subheader("🎋 Generated Kanbun Poem:")
                st.write(kanbun)

                st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                st.subheader("📖 Converted Japanese Text:")
                st.write(japanese_text)

                st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                st.subheader(f"🌐 Translation to {target_language}:")
                st.write(translation)

                st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                st.subheader(f"📚 Key Vocabulary in {target_language} (with JLPT levels and examples):")
                st.write(vocabulary)

                st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                # Prepare data for table and export
                data = {
                    "Input Sentence/Passage": [sentence],
                    "Kanbun Poem": [kanbun],
                    "Converted Japanese Text": [japanese_text],
                    f"Translation to {target_language}": [translation],
                    f"Key Vocabulary in {target_language} (with JLPT levels and examples)": [vocabulary]
                }
                df = pd.DataFrame(data)

                st.subheader("📊 Poem Details in Table Format:")
                st.dataframe(df)

                excel = BytesIO()

                with pd.ExcelWriter(excel, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name="Kanbun")
                excel.seek(0)

                st.download_button(
                    label="📏 Download as CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="kanbun_data.csv",
                    mime="text/csv"
                )

                st.download_button(
                    label="📄 Download as Excel",
                    data=excel,
                    file_name="kanbun_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="kanbun_data_download"
                )
            except Exception as e:
                st.warning("⚠️ Incorrect API key provided ⚠️")
        else:
            st.warning("⚠️ Please enter a sentence or passage to generate a poem ⚠️")

    st.markdown(
        """
        <hr style="border: 1px solid #D3D3D3; margin-top: 50px;">
        <p style="text-align: center; font-size: 0.9em; color: #555;">
            Made with 💖 | 
            Check out & ⭐️ <a href="https://github.com/Pcttt/Kanbun-Generater" target="_blank" style="color: #1E90FF; text-decoration: none;">GitHub Repo</a>
        </p>
        <p style="text-align: center; font-size: 0.8em; color: #555;">
            Powered by 🔋 Streamlit & OpenAI
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
