const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");

function addMessage(text, sender) {
    const msgEl = document.createElement("div");
    msgEl.classList.add("message", sender);

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;

    msgEl.appendChild(bubble);
    messagesEl.appendChild(msgEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addTypingIndicator() {
    const msgEl = document.createElement("div");
    msgEl.classList.add("message", "bot");
    msgEl.id = "typing-msg";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    const typing = document.createElement("div");
    typing.classList.add("typing");
    typing.innerHTML = `
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
    `;

    bubble.appendChild(typing);
    msgEl.appendChild(bubble);
    messagesEl.appendChild(msgEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTypingIndicator() {
    const typing = document.getElementById("typing-msg");
    if (typing) {
        typing.remove();
    }
}

async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    addMessage(text, "user");
    inputEl.value = "";

    addTypingIndicator();

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        removeTypingIndicator();
        addMessage(data.answer, "bot");
    } catch (err) {
        removeTypingIndicator();
        addMessage("Error contacting the assistant backend.", "bot");
        console.error(err);
    }
}

sendBtn.addEventListener("click", sendMessage);

inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

newChatBtn.addEventListener("click", () => {
    messagesEl.innerHTML = "";
    addMessage(
        "New chat started. Ask me about VPN, Wi-Fi, Outlook, or your laptop issues.",
        "bot"
    );
});
