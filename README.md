AI Chatbot 2025
================

Overview
--------

AI Chatbot 2025 is a small, beginner‑friendly conversational assistant that runs on a lightweight Flask backend with a LLaMA‑style model wrapper.  
The chatbot keeps short‑term conversation history so it can give simple, domain‑aware answers in real time.

Key Features
------------

- **Domain‑aware conversational AI**: Wraps a small LLaMA‑style model in PyTorch, with a safe fallback to a rule‑based engine so it also runs on low‑spec machines.
- **Real‑time web interface**: Flask backend plus a clean JavaScript frontend for responsive, context‑aware chat.
- **Low‑latency, lightweight design**: Keeps inference and context handling simple for fast responses and easier deployment.

How it Works
------------

- **Backend (`app.py`)**
  - Exposes a `/` route that serves the chat UI.
  - Exposes a `/api/chat` endpoint that accepts JSON:
    - `message`: the latest user message.
    - `history`: recent chat history (user + assistant turns).
  - Sends the message and history into `LlamaChatModel` and returns the generated reply.

- **Model wrapper (`model.py`)**
  - Tries to load a small LLaMA‑style chat model with `transformers` and PyTorch.
  - If a model can’t be loaded (no GPU, limited RAM, or offline), it falls back to a beginner‑friendly rule‑based engine so the project is still fully usable.
  - Keeps the API simple: one main method, `generate_reply(message, history)`.

- **Frontend (`templates/index.html`, `static/app.js`, `static/styles.css`)**
  - Minimal single‑page chat UI.
  - Sends messages to `/api/chat` using `fetch` and renders responses in a chat bubble layout.
  - Maintains a small in‑browser copy of the conversation (`history`) for context‑aware replies.

Getting Started
---------------

1. **Create and activate a virtual environment (recommended)**

   ```bash
   cd "E:\python\ai chatbot"
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app**

   ```bash
   python app.py
   ```

4. **Open the chat UI**

   - In your browser, go to: `http://127.0.0.1:5000`
   - Type a message and press **Enter** or click **Send**.

Notes on the Model
------------------

- By default, `LlamaChatModel` is configured to use:

  - `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (a small, LLaMA‑style chat model)  
    via the Hugging Face `transformers` library.

- If this model cannot be downloaded or loaded (for example, due to limited hardware), the project automatically switches to a rule‑based reply system:

  - You still get a working chatbot.
  - The overall architecture (Flask + model wrapper + JS client) stays the same, making it easy to plug in a fine‑tuned LLaMA model later.

Resume‑Style Description
------------------------

- **Built an advanced conversational AI chatbot powered by a LLaMA‑style PyTorch model for domain‑specific, context‑aware responses.**
- **Developed a Flask + JavaScript web interface enabling real‑time chat with short‑term conversation memory.**
- **Optimized for low‑latency inference on a lightweight backend, making the system easy to deploy and scale.**


