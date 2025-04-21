import streamlit as st
from transformers import pipeline
import requests

# Lazy loading of the model
def load_model():
    return pipeline("text-generation", model="gpt2")

# Function to fetch book content from an API (like Google Books API)
def fetch_book_content(book_title, author_name):
    # Example: Use a public API like Google Books API to fetch book content
    query = f"{book_title} {author_name}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    
    response = requests.get(url).json()
    if 'items' in response:
        # Get the first book's description
        book = response['items'][0]['volumeInfo']
        description = book.get('description', 'No description available')
        return description
    else:
        return "Sorry, I couldn't find any content for this book."

# Function to generate a prompt based on the content of the book
def generate_prompt(book_title, book_content):
    prompt = f"""
    You are a professor asking a student to write a paper on the following book:
    Title: {book_title}

    Book content (summary or excerpt): {book_content}

    Based on this content, ask the student a detailed, open-ended question about the book. 
    The question should require a deep understanding of the book's themes, characters, or events.
    """
    return prompt

# Function to grade the content, grammar, and writing style using Hugging Face's model
def grade_paper(text, book_title):
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

# Input for the book title and author
book_title = st.text_input("Enter the title of the book you've read:")
author_name = st.text_input("Enter the author of the book:")

# When the user provides the book title and author
if book_title and author_name:
    # Fetch the book content (summary or excerpt)
    book_content = fetch_book_content(book_title, author_name)
    
    if book_content:
        # Generate a prompt based on the book content
        generated_prompt = generate_prompt(book_title, book_content)
        
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
        st.warning("Could not fetch the content for this book. Please try again later.")
else:
    st.info("Please provide both the book title and author to generate a prompt.")
