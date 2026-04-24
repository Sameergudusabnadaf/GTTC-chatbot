import os
import re
import requests
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from openai import OpenAI

# ================= CONFIG =================

NVIDIA_API_KEY = "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"
BASE_URL = "https://gttc.karnataka.gov.in/86/magadi-stu-36/en"

# DeepSeek Setup
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

app = Flask(__name__)

# ================= WEBSITE SCRAPER =================

def scrape_page(url):

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text

    except:
        return ""

print("Scraping GTTC Website...")

website_data = scrape_page(BASE_URL)

print("Website data loaded")

# ================= DEEPSEEK AI =================

def ask_ai(question):

    prompt = f"""
You are an AI assistant for GTTC Magadi Institute.

Website Information:
{website_data[:12000]}

User Question:
{question}

Answer clearly and shortly. Provide ONLY the final answer to the user. DO NOT output your internal thoughts or reasoning. Do NOT use <think> tags.
"""

    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1-distill-llama-8b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True
    )

    # Stream the reply and collect it
    reply = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            reply += chunk.choices[0].delta.content

    # Manually remove <think> blocks
    # <think> is at the start, </think> might be missing.
    if '<think>' in reply and '</think>' in reply:
        reply = reply.split('</think>')[-1].strip()
    elif '<think>' in reply:
        # If it started a think block but never finished it, we can't extract an answer.
        # Deepseek distills sometimes fail to close it. Let's just provide a fallback.
        reply = "Hello! I am ready to help you with GTTC Magadi."
        
    return reply


# ================= API =================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    question = data.get("message")

    answer = ask_ai(question)

    return jsonify({"reply": answer})


# ================= WEB UI =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= RUN =================

if __name__ == "__main__":
    app.run(port=5000, debug=True)