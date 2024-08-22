from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

def scrape_faq_content(url):
    print("Scraping FAQ content from URL...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    faqs = []

    for question in soup.select('div.cmp-accordion__title'):
        answer = question.find_next_sibling('div')
        if answer:
            faqs.append({
                'question': question.get_text(strip=True),
                'answer': answer.get_text(strip=True)
            })


    print("Scraped FAQs:")
    for faq in faqs:
        print(f"Question: {faq['question']}")
        print(f"Answer: {faq['answer']}")
    return faqs

# URL FAQ
faq_url = "https://help-qa.pge.com/s/article/Why-is-my-gas-bill-so-high?language=en_US"
faq_content = scrape_faq_content(faq_url)

def get_answer(question):
    print(f"Received question: {question}")
    
    if "how i pay bill" in question.lower():
        return "You can pay your bill online through our website, by mail, or at one of our authorized payment locations."

    # Logika pencarian FAQ
    question_lower = question.lower()
    for faq in faq_content:
        faq_question_lower = faq['question'].lower()
        if question_lower in faq_question_lower:
            return faq['answer']
    
    return "I'm sorry, I couldn't find an answer to your question."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    print(f"Form data received: {request.form}")
    if not question:
        return jsonify({"response": "No question provided."})
    response = get_answer(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
