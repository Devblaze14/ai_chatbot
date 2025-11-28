const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

let history = [];
let isSending = false;

function appendMessage(role, content) {
  const row = document.createElement("div");
  row.className = `message-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role}`;
  avatar.textContent = role === "user" ? "You" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);

  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  if (!message || isSending) return;

  isSending = true;
  sendButton.disabled = true;

  appendMessage("user", message);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        history,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const msg =
        (errorData && errorData.error) ||
        "The server could not process your request.";
      appendMessage("assistant", msg);
      return;
    }

    const data = await response.json();
    const reply = data.reply || "I could not generate a reply this time.";
    history = data.history || [];

    appendMessage("assistant", reply);
  } catch (err) {
    appendMessage(
      "assistant",
      "Network error: please check that the Flask server is running and try again."
    );
  } finally {
    isSending = false;
    sendButton.disabled = false;
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;
  messageInput.value = "";
  sendMessage(message);
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.dispatchEvent(new Event("submit"));
  }
});

// Initial greeting so the UI does not look empty.
appendMessage(
  "assistant",
  "Welcome! I’m your AI Chatbot 2025. Ask a question or describe your task, and I’ll respond with a short, clear explanation."
);


