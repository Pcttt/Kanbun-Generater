import openai
import streamlit as st

# Sidebar for OpenAI API Key
st.sidebar.title("Settings")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
    st.stop()

openai.api_key = openai_api_key

# Function to generate Kanbun
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

# Streamlit app UI
def main():
    st.title("Kanbun (\u6f22\u6587) Text Generator")

    st.subheader("Enter Text to Convert to Kanbun")
    user_input = st.text_area("Input Text:", placeholder="Type or paste your text here...")

    if st.button("Generate Kanbun"):
        if user_input.strip():
            with st.spinner("Generating Kanbun..."):
                kanbun_result = generate_kanbun(user_input)
            
            st.subheader("Generated Kanbun:")
            st.write(kanbun_result)
        else:
            st.warning("Please enter some text to convert.")

if __name__ == "__main__":
    main()
