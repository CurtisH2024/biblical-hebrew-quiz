import streamlit as st
import requests
import ssl
import certifi
import re

# SSL fix for some Windows/conda environments
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_default_https_context or ssl.create_default_context

# Load Hugging Face API key securely
HF_API_KEY = st.secrets["hugging_face_api_key"]
HF_MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b"

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

# Page setup
st.set_page_config(page_title="Biblical Hebrew Quiz", layout="centered")
st.title("📜 Biblical Hebrew Reading Comprehension Quiz")

book = st.selectbox("📖 Select Book of the Bible:", bible_books)
chapter = st.number_input("📄 Chapter Number:", min_value=1, step=1)
num_questions = st.slider("🔢 Number of Questions", min_value=3, max_value=10, value=5)

def call_model(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    response = requests.post(HF_MODEL_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    output = response.json()
    return output[0]["generated_text"] if isinstance(output, list) else output.get("generated_text", "")

def parse_quiz(quiz_text):
    pattern = r"\d+[.)]\s*(.*?)\n(?:-?\s?[א-ד]\.?\s.*\n?)+"
    questions = re.findall(pattern, quiz_text, re.DOTALL)
    
    qa_blocks = re.split(r"\n(?=\d+[.)])", quiz_text)
    quiz_data = []

    for block in qa_blocks:
        q_match = re.match(r"\d+[.)]\s*(.*?)\n", block)
        if not q_match:
            continue
        question = q_match.group(1).strip()

        options = re.findall(r"[א-ד]\.?\s(.*)", block)
        correct_option = options[0] if options else None  # Assuming the first one is correct
        quiz_data.append({
            "question": question,
            "options": options,
            "correct": correct_option
        })

    return quiz_data

if st.button("Generate Quiz"):
    with st.spinner("📜 Generating quiz..."):

        prompt = f"""
אתה מורה ללשון מקראית. כתוב שאלון הבנת הנקרא על פרק {chapter} מתוך ספר {book}.
השאלון צריך לכלול {num_questions} שאלות.
השתמש בעברית מקראית בלבד (כולל ניקוד מלא), שאל שאלות פרטניות על תוכן הפרק.
הצג כל שאלה בצורה של שאלה אמיתית.
עבור כל שאלה, הצג ארבע אפשרויות – רק אחת מהן נכונה. 
ציין את האפשרות הנכונה ראשונה בכל מקרה.
אל תציג את הפסוקים עצמם.
"""

        try:
            result_text = call_model(prompt)
            quiz = parse_quiz(result_text)

            st.markdown("### ✍️ המבחן שלך:")
            score = 0

            for idx, q in enumerate(quiz):
                st.markdown(f"**{idx+1}. {q['question']}**")
                selected = st.radio(
                    f"שאלה {idx+1}",
                    options=q["options"],
                    key=f"q{idx}"
                )

                if st.button(f"בדוק תשובה {idx+1}", key=f"btn{idx}"):
                    if selected == q["correct"]:
                        st.success("✅ תשובה נכונה!")
                        score += 1
                    else:
                        st.error(f"❌ שגוי. התשובה הנכונה היא: {q['correct']}")

            st.markdown("---")
            st.markdown(f"**ציון סופי: {score} מתוך {len(quiz)}**")

        except Exception as e:
            st.error(f"❌ Error generating or displaying quiz:\n\n{e}")
