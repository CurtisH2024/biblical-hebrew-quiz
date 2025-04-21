import streamlit as st
from transformers import pipeline

# Lazy loading of the model
def load_model():
    return pipeline("text-generation", model="gpt2")

# Function to grade the content, grammar, and writing style using Hugging Face's model
def grade_paper(text, book_content):
    # Combine book content with the input to give context
    prompt = f"""
    You are a professor grading a paper based on a book that was written by the user.
    Please evaluate the following submission based on the content, grammar, and writing style.

    Book content: {book_content}

    The student's submission: {text}

    1. Rate the content out of 100, considering its relevance, originality, and clarity.
    2. Rate the grammar out of 100, considering the correctness, sentence structure, and punctuation.
    3. Rate the writing style out of 100, considering tone, readability, and engagement.

    Provide a detailed breakdown of the grades and an overall assessment.
    """
    
    # Use the Hugging Face model to generate a response based on the prompt
    result = text_generator(prompt, max_length=500, num_return_sequences=1)
    
    # Return the model's generated feedback
    return result[0]['generated_text'].strip()

# Streamlit UI
st.title("Paper Grader with Hugging Face")

# Input for book content (optional)
book_content = st.text_area("Enter the content of your book (optional)", height=300)

# Input for the student submission (paper)
student_submission = st.text_area("Enter your submission", height=300)

# When the user submits the form
if st.button("Grade My Paper"):
    if student_submission.strip() != "":
        # Load the model lazily
        text_generator = load_model()

        # Grade the paper
        grade_response = grade_paper(student_submission, book_content)
        st.write("### Grading Result:")
        st.write(grade_response)
    else:
        st.warning("Please enter your submission before grading.")
