import streamlit as st
from transformers import pipeline

# Lazy loading of the model
def load_model():
    return pipeline("text-generation", model="gpt2")

# Function to generate a prompt based on the book title alone
def generate_prompt(book_title):
    prompt = f"""
    You are a professor asking a student to write a paper based on the following book:
    Title: {book_title}

    Based on the book's title and general knowledge, ask the student a thoughtful, open-ended question that could be answered after reading the book.
    """
    return prompt

# Function to grade the content, grammar, and writing style using Hugging Face's model
def grade_paper(text, book_title):
    # Combine book title with the input to give context
    prompt = f"""
    You are a professor grading a paper based on the book titled: {book_title}.
    Please evaluate the following submission based on the content, grammar, and writing style.

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
st.title("Book-Based Paper Grader with Hugging Face (Self-Test)")

# Input for the book title
book_title = st.text_input("Enter the title of the book you've read:")

# When the user provides the book title
if book_title:
    # Generate a prompt based on the book's title
    generated_prompt = generate_prompt(book_title)
    
    # Display the generated prompt
    st.write("### Generated Prompt for You:")
    st.write(generated_prompt)
    
    # Input for the student submission (response to the prompt)
    student_submission = st.text_area("Enter your response to the prompt", height=300)
    
    # When the user submits their response
    if st.button("Grade My Paper"):
        if student_submission.strip() != "":
            # Load the model lazily
            text_generator = load_model()

            # Grade the paper based on the response
            grade_response = grade_paper(student_submission, book_title)
            st.write("### Grading Result:")
            st.write(grade_response)
        else:
            st.warning("Please enter your response before grading.")
else:
    st.info("Please provide the book title to generate a prompt.")
