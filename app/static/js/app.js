document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const messages = document.getElementById("chat-messages");
  const input = document.getElementById("chat-input");
  const clear = document.getElementById("clear-chat");
  if (!form || !messages || !input) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    messages.insertAdjacentHTML("beforeend", `<div class="chat-message user"><span class="chat-avatar">${message.charAt(0).toUpperCase()}</span><div>${escapeHtml(message)}</div></div>`);
    input.value = "";
    const response = await fetch("/api/ai/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
      body: JSON.stringify({message})
    });
    const data = await response.json();
    if (!response.ok) {
      messages.insertAdjacentHTML("beforeend", `<div class="alert alert-danger">${escapeHtml(data.error || "Unable to send message.")}</div>`);
      return;
    }
    messages.insertAdjacentHTML("beforeend", `<div class="chat-message assistant"><span class="chat-avatar">✧</span><div>${escapeHtml(data.reply)}</div></div>`);
  });
  clear?.addEventListener("click", async () => {
    await fetch("/api/ai/clear", {method: "POST", headers: {"X-CSRFToken": getCsrfToken()}});
    messages.innerHTML = '<div class="empty-state"><span class="empty-icon">✧</span><h3>Ask anything about your cloud</h3><p>Docker, AWS, Terraform, CI/CD and DevSecOps guidance in one place.</p></div>';
  });
});

function getCsrfToken() {
  return document.querySelector('input[name="csrf_token"]')?.value || "";
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value;
  return element.innerHTML;
}

