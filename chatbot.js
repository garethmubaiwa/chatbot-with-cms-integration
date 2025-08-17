const sendButton = document.getElementById("sendButton");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");
const fileUpload = document.getElementById("fileUpload");
const chatbotButton = document.getElementById("chatbot-button");
const chatWindow = document.getElementById("chatWindow");
const closeChat = document.getElementById("closeChat");

function addMessage(message, sender = "bot") {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.innerText = message;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message }),
    });
    const data = await response.json();
    addMessage(data.answer || "Sorry, I couldn't find an answer.", "bot");
  } catch {
    addMessage("Error connecting to server.", "bot");
  }
}

async function uploadFile() {
  const file = fileUpload.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    addMessage(data.message || "File uploaded successfully!", "bot");
  } catch {
    addMessage("File upload failed.", "bot");
  }
}

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Upload as soon as user picks file
fileUpload.addEventListener("change", uploadFile);

// Open chat
chatbotButton.addEventListener("click", () => {
  chatWindow.classList.toggle("hidden");
});

// Close chat
closeChat.addEventListener("click", () => {
  chatWindow.classList.add("hidden");
});
