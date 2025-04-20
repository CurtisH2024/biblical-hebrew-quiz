import streamlit as st
import requests

# Load Hugging Face API key securely
HF_API_KEY = st.secrets["hugging_face_api_key"]

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

# Streamlit UI
st.set_page_config(page_title="Biblical Hebrew Quiz Generator", layout="centered")
st.title("📜 Biblical Hebrew Reading Comprehension Quiz")

book = st.selectbox("📖 Select Book of the Bible:", bible_books)
chapter = st.number_input("📄 Chapter Number:", min_value=1, step=1)
num_questions = st.slider("🔢 Number of Questions", min_value=3, max_value=10, value=5)

if st.button("Generate Quiz"):
    with st.spinner("Generating quiz..."):
        try:
            prompt = f"""
אתה מורה ללשון מקראית. כתוב שאלון הבנת הנקרא על פרק {chapter} מתוך ספר {book}.
השאלון צריך לכלול {num_questions} שאלות.
השתמש בעברית מקראית בלבד (כולל ניקוד מלא), שאל שאלות פרטניות על תוכן הפרק.
הצג כל שאלה בצורה של שאלה אמיתית, וכל תשובה כאפשרות משפטית, לא כשאלה.
עבור כל שאלה הצג ארבע אפשרויות – רק אחת מהן נכונה.
אל תציג את הפסוקים עצמם.
"""

            # Call Hugging Face inference API
            headers = {
                "Authorization": f"Bearer {HF_API_KEY}"
            }

            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 700, "temperature": 0.7},
                "options": {"wait_for_model": True}
            }

            response = requests.post(
                "https://api-inference.huggingface.co/models/bigscience/bloom-1b1",  # You can change to another model
                headers=headers,
                json=payload
            )

            result = response.json()

            if "error" in result:
                st.error(f"❌ API Error: {result['error']}")
            else:
                generated_text = result[0]["generated_text"]
                # Extract only the part after the prompt
                quiz_text = generated_text[len(prompt):].strip()
                st.markdown("### ✍️ המבחן שלך:")
                st.markdown(quiz_text)

        except Exception as e:
            st.error(f"❌ Error generating quiz:\n\n{e}")
