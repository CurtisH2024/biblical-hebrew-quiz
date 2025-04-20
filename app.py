import streamlit as st
import requests
import ssl
import certifi

# SSL fix for some Windows/conda environments
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_default_https_context or ssl.create_default_context

# Load Hugging Face API key securely from Streamlit secrets
HF_API_KEY = st.secrets["hugging_face_api_key"]

# Use a faster model that's less likely to timeout
HF_MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b"

# List of books in the Bible
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

# Streamlit UI setup
st.set_page_config(page_title="Biblical Hebrew Quiz Generator", layout="centered")
st.title("📜 Biblical Hebrew Reading Comprehension Quiz")

book = st.selectbox("📖 Select Book of the Bible:", bible_books)
chapter = st.number_input("📄 Chapter Number:", min_value=1, step=1)
num_questions = st.slider("🔢 Number of Questions", min_value=3, max_value=10, value=5)

if st.button("Generate Quiz"):
    with st.spinner("🛠️ Generating quiz using Hugging Face..."):

        prompt = f"""
אתה מורה ללשון מקראית. כתוב שאלון הבנת הנקרא על פרק {chapter} מתוך ספר {book}.
השאלון צריך לכלול {num_questions} שאלות.
השתמש בעברית מקראית בלבד (כולל ניקוד מלא), שאל שאלות פרטניות על תוכן הפרק.
הצג כל שאלה בצורה של שאלה אמיתית, וכל תשובה כאפשרות משפטית, לא כשאלה.
עבור כל שאלה הצג ארבע אפשרויות – רק אחת מהן נכונה.
אל תציג את הפסוקים עצמם.
"""

        headers = {
            "Authorization": f"Bearer {HF_API_KEY}"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
            },
            "options": {
                "wait_for_model": True
            }
        }

        try:
            response = requests.post(HF_MODEL_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                quiz_text = result[0]["generated_text"].strip()
            elif isinstance(result, dict) and "error" in result:
                raise Exception(result["error"])
            else:
                quiz_text = result.get("generated_text", "⚠️ No output received.")

            st.markdown("### ✍️ המבחן שלך:")
            st.markdown(quiz_text)

        except Exception as e:
            st.error(f"❌ Error generating quiz:\n\n{e}")
