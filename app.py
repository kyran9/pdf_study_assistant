# pdf_study_assistant.py

import os
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import PyPDF2

# --- Ensure NLTK punkt tokenizer is available ---
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    print("Downloading NLTK 'punkt' tokenizer...")
    nltk.download("punkt")

# --- Function to read PDF text ---
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# --- Function to summarize text ---
def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return [str(sentence) for sentence in summary]

# --- Function to generate simple quiz questions ---
def generate_quiz(text):
    from nltk.tokenize import sent_tokenize, word_tokenize
    import random

    sentences = sent_tokenize(text)
    quiz = []

    for sent in sentences:
        words = word_tokenize(sent)
        if len(words) > 5:
            blank_word = random.choice(words)
            question = sent.replace(blank_word, "_____")
            answer = blank_word
            quiz.append({"question": question, "answer": answer})
        if len(quiz) >= 5:
            break
    return quiz

# --- Main program ---
if __name__ == "__main__":
    print("📄 PDF Study Assistant\n")
    pdf_path = input("👉 Enter full path to PDF file: ").strip()

    if not os.path.exists(pdf_path):
        print("\n❌ File not found. Check the path and try again.")
        exit()

    print("\n🔍 Reading PDF...")
    text = read_pdf(pdf_path)

    print("\n📘 Summary:\n")
    summary = summarize_text(text, sentence_count=5)
    for i, sentence in enumerate(summary, 1):
        print(f"{i}. {sentence}")

    print("\n📝 Quiz Questions:\n")
    quiz = generate_quiz(text)
    for i, q in enumerate(quiz, 1):
        print(f"Q{i}: {q['question']}")
        print(f"A{i}: {q['answer']}\n")
