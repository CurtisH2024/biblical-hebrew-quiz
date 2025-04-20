import streamlit as st
import openai
import ssl
import certifi

# SSL fix (optional but recommended for some environments)
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_default_https_context or ssl.create_default_context

# Load OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# List of books in the Bible
bible_books = [
    "בראשית", "שמות", "ויקרא", "במדבר", "דברים",
    "יהושע", "שופטים", "רות", "שמואל א", "שמואל ב",
    "מלכים א", "מלכים ב", "ישעיהו", "ירמיהו", "יחזקאל",
    "הושע", "יואל", "עמוס", "עובדיה", "יונה",
    "מיכה", "נחום", "חבקוק", "צפניה", "חגי",
    "זכריה", "מלאכי", "תהילים", "משלי", "איוב",
    "שיר השירים", "רות", "איכה", "כוהלת", "אסתר",
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

            # Correct method for OpenAI v1+ library
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "אתה מורה ללשון מקראית."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            quiz_text = response.choices[0].message.content.strip()
            st.markdown("### ✍️ המבחן שלך:")
            st.markdown(quiz_text)

        except Exception as e:
            st.error(f"❌ Error generating quiz:\n\n{e}")
