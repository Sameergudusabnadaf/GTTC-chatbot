 # GTTC-chatbot

A Flask-based AI Chatbot designed to answer questions related to the GTTC Magadi Institute. It scrapes the official website for context and uses the DeepSeek AI model (via NVIDIA API) to generate accurate responses.

## 🚀 Workflow (Step-by-Step)

### Step 1: Prerequisites

Ensure you have Python installed on your system. You will also need the following Python packages:

- `flask`
- `requests`
- `beautifulsoup4`
- `openai`

You can install them using pip:

```bash
pip install flask requests beautifulsoup4 openai
```

### Step 2: Setup the Project

Navigate to the project directory containing the chatbot script:

```bash
cd sam4
```

### Step 3: Run the Application

Start the Flask server by running the `chatbot.py` script:

```bash
python chatbot.py
```

_Note: The script will automatically scrape the GTTC website to gather the latest context before starting the server._

### Step 4: Access the Web UI

Once the server is running, open your web browser and go to:

```
http://127.0.0.1:5000/
```

You can now interact with the GTTC-chatbot!

---

**Developed by Sameer Nadaf**
