# app.py

import streamlit as st
import openai
import ssl
import certifi

# SSL fix for some Windows/conda environments
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_default_https_context or ssl.create_default_context

# Load OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# List of books in the Bible (you can extend this list as needed)
bible_books = [
    "בראשית", "שמות", "ויקרא", "במדבר", "דברים",  # Genesis, Exodus, Leviticus, Numbers, Deuteronomy
    "יהושע", "שופטים", "רות", "שמואל א", "שמואל ב",  # Joshua, Judges, Ruth, 1 Samuel, 2 Samuel
    "מלכים א", "מלכים ב", "ישעיהו", "ירמיהו", "יחזקאל",  # 1 Kings, 2 Kings, Isaiah, Jeremiah, Ezekiel
    "הושע", "יואל", "עמוס", "עובדיה", "יונה",  # Hosea, Joel, Amos, Obadiah, Jonah
    "מיכה", "נחום", "חבקוק", "צפניה", "חגי",  # Micah, Nahum, Habakkuk, Zephaniah, Haggai
    "זכריה", "מלאכי", "תהילים", "משלי", "איוב",  # Zechariah, Malachi, Psalms, Proverbs, Job
    "שיר השירים", "רות", "איכה", "כוהלת", "אסתר",  # Song of Songs, Ruth, Lamentations, Ecclesiastes, Esther
    "דניאל", "עזרא", "נחמיה", "דברי הימים א", "דברי הימים ב"  # Daniel, Ezra, Nehemiah, 1 Chronicles, 2 Chronicles
]

# Streamlit UI
st.set_page_config(page_title="Biblical Hebrew Quiz Generator", layout="centered")
st.title("📜 Biblical Hebrew Reading Comprehension Quiz")

# Dropdown for book selection
book = st.selectbox("📖 Select Book of the Bible:", bible_books)

# User input for chapter
chapter = st.number_input("📄 Chapter Number:", min_value=1, step=1)

# Number of questions
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

            # Make OpenAI request using the API
            response = openai.Completion.create(
                model="text-davinci-003",  # You can replace with another model if preferred
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
            )

            quiz_text = response.choices[0].text.strip()  # Adjust based on the response structure
            st.markdown("### ✍️ המבחן שלך:")
            st.markdown(quiz_text)

        except Exception as e:
            st.error(f"❌ Error generating quiz:\n\n{e}")
