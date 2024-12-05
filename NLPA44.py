import openai
import streamlit as st
import pandas as pd

# ตั้งค่า API key ของ OpenAI
# ตั้งค่า API Key

openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
# ตรวจสอบการเชื่อมต่อ OpenAI API
if openai_api_key:
   openai.api_key = 'your-api-key'

# ฟังก์ชันในการสร้างกลอนคันบุน (漢文) โดยใช้ OpenAI API (ChatCompletion)
def generate_kanbun(prompt):
    # ส่งคำขอไปยัง ChatGPT เพื่อสร้างกลอน
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # หรือ "gpt-4" ถ้าคุณต้องการใช้ GPT-3.5
        messages=[{"role": "system", "content": "คุณคือผู้แต่งกลอนคันบุน (漢文) ที่มีความเชี่ยวชาญ"},
                  {"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    
    kanbun = response.choices[0].message.content.strip()
    return kanbun

# ฟังก์ชันในการแปล漢文 เป็นภาษาอังกฤษ
def translate_kanbun_to_english(kanbun):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "คุณคือผู้เชี่ยวชาญด้านการแปล漢文เป็นภาษาอังกฤษ"},
                  {"role": "user", "content": f"แปลข้อความ漢文นี้เป็นภาษาอังกฤษ: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    
    translation = response.choices[0].message.content.strip()
    return translation

# ฟังก์ชันเพื่อดึงคำศัพท์ที่น่าสนใจจาก漢文
def extract_vocabulary(kanbun):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "คุณคือผู้เชี่ยวชาญด้านคำศัพท์จาก漢文"},
                  {"role": "user", "content": f"ช่วยรวบรวมคำศัพท์ที่น่าสนใจจากข้อความ漢文นี้: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    
    vocabulary = response.choices[0].message.content.strip()
    return vocabulary

# ฟังก์ชันที่จัดการการแสดงผลลัพธ์ใน Streamlit
def main():
    st.title("AI poem 漢文 (Kanbun)")

    theme = st.text_input("input here")

    if st.button("generate"):
        if theme:
            prompt = f"สร้างกลอนคันบุน (漢文) ที่เกี่ยวข้องกับ {theme}"
            kanbun = generate_kanbun(prompt)

            # แปล漢文เป็นภาษาอังกฤษ
            translation = translate_kanbun_to_english(kanbun)

            # รวบรวมคำศัพท์ที่น่าสนใจ
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("กลอนคันบุนที่สร้างขึ้น:")
            st.write(kanbun)

            st.subheader("การแปลเป็นภาษาอังกฤษ:")
            st.write(translation)

            st.subheader("คำศัพท์ที่น่าสนใจจาก漢文:")
            st.write(vocabulary)

            data = {
                "ธีม": [theme],
                "กลอนคันบุน": [kanbun],
                "แปลเป็นภาษาอังกฤษ": [translation],
                "คำศัพท์ที่น่าสนใจ": [vocabulary]
            }
            df = pd.DataFrame(data)

            # แสดง DataFrame
            st.subheader("ข้อมูลในรูปแบบตาราง:")
            st.dataframe(df)

            # ปุ่มดาวน์โหลดข้อมูลเป็น CSV
            st.download_button(
                label="ดาวน์โหลดข้อมูลเป็น CSV",
                data=df.to_csv(index=False),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            # ปุ่มดาวน์โหลดข้อมูลเป็น Excel
            st.download_button(
                label="ดาวน์โหลดข้อมูลเป็น Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("กรุณาระบุธีมของกลอนเพื่อสร้าง")

if __name__ == "__main__":
    main()
