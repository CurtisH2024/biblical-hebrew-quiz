import streamlit as st
import requests
import ssl
import certifi
import re
import random

# SSL fix (for some environments)
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_default_https_context or ssl.create_default_context

# Load Hugging Face API key
HF_API_KEY = st.secrets["hugging_face_api_key"]
HF_MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/google/flan-t5-large"

# List of Bible books
bible_books = [
    "בראשית", "שמות", "ויקרא", "במדבר", "דברים",
    "יהושע", "שופטים", "רות", "שמואל א", "שמואל ב",
    "מלכים א", "מלכים ב", "ישעיהו", "ירמיהו", "יחזקאל",
    "הושע", "יואל", "עמוס", "עובדיה", "יונה",
    "מיכה", "נחום", "חבקוק", "צפניה", "חגי",
    "זכריה", "מלאכי", "תהילים", "משלי", "איוב",
    "שיר השירים", "איכה", "קהלת", "אסתר",
    "דניאל", "עזרא", "נחמיה", "דברי הימים א", "דברי הימים ב"
]

# Streamlit app config
st.set_page_config(page_title="Biblical Hebrew Quiz", layout="centered")
st.title("📜 Biblical Hebrew Reading Comprehension Quiz")

book = st.selectbox("📖 Select Book of the Bible:", bible_books)
chapter = st.number_input("📄 Chapter Number:", min_value=1, step=1)
num_questions = st.slider("🔢 Number of Questions", min_value=3, max_value=10, value=5)

def call_model(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 512, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }
    response = requests.post(HF_MODEL_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    output = response.json()
    return output[0]["generated_text"] if isinstance(output, list) else output.get("generated_text", "")

def parse_quiz(raw_text):
    qa_blocks = re.split(r"\n(?=\d+[.)])", raw_text.strip())
    quiz_data = []

    for block in qa_blocks:
        question_match = re.search(r"\d+[.)]\s*(.*?)\n", block)
        if not question_match:
            continue
        question = question_match.group(1).strip()

        options = re.findall(r"[א-ד]\.?\s(.*)", block)
        if not options or len(options) < 4:
            continue

        correct = options[0]
        random.shuffle(options)

        quiz_data.append({
            "question": question,
            "options": options,
            "correct": correct
        })
    return quiz_data

if st.button("Generate Quiz"):
    with st.spinner("📜 Generating quiz..."):

        prompt = f"""
כתוב {num_questions} שאלות הבנת הנקרא על פרק {chapter} מתוך ספר {book}, בעברית מקראית עם ניקוד.
עבור כל שאלה, הצג ארבע תשובות אפשריות (א. ב. ג. ד.), ורק אחת מהן נכונה והיא הראשונה.
אל תציין את הפסוקים עצמם.
"""

        try:
            result_text = call_model(prompt)
            quiz = parse_quiz(result_text)

            if not quiz:
                st.warning("⚠️ לא נמצאו שאלות תקפות. ייתכן שהמודל לא הגיב כראוי.")
            else:
                st.markdown("### ✍️ המבחן שלך:")
                score = 0

                for idx, q in enumerate(quiz):
                    st.markdown(f"**{idx+1}. {q['question']}**")
                    user_answer = st.radio(
                        label="בחר תשובה:",
                        options=q["options"],
                        key=f"q_{idx}"
                    )
                    if st.button(f"בדוק שאלה {idx+1}", key=f"check_{idx}"):
                        if user_answer == q["correct"]:
                            st.success("✅ תשובה נכונה!")
                            score += 1
                        else:
                            st.error(f"❌ שגוי. התשובה הנכונה היא: {q['correct']}")

                st.markdown("---")
                st.markdown(f"**📊 ציון סופי: {score} מתוך {len(quiz)}**")

        except Exception as e:
            st.error(f"❌ Error generating or displaying quiz:\n\n{e}")
