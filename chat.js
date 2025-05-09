// Enhanced chat widget with left/right alignment, markdown, typing animation, and minimize button
let chatMinimized = true; // Start minimized by default
const chatHistory = [];
let typingInterval = null;
let typingDiv = null;

function renderMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\*(.*?)\*/g, '<i>$1</i>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
        .replace(/\n/g, '<br>');
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    addMessage('user', message);
    input.value = '';
    showTyping();
    const response = await fetch('https://riyazat-blog.onrender.com/chat-api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const data = await response.json();
    hideTyping();
    addMessage('riyazat', data.reply);
}

function addMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg ' + (sender === 'user' ? 'user-msg' : 'ai-msg');
    msgDiv.innerHTML = sender === 'user'
        ? `<div class="msg-bubble user-bubble">${renderMarkdown(text)}</div>`
        : `<div class="msg-bubble ai-bubble">${renderMarkdown(text)}</div>`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
    const chatBox = document.getElementById('chat-box');
    typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg ai-msg';
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble ai-bubble';
    bubble.id = 'typing-bubble';
    bubble.innerText = 'Riyazat is typing';
    typingDiv.appendChild(bubble);
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    let dots = 0;
    typingInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        bubble.innerText = 'Riyazat is typing' + '.'.repeat(dots);
    }, 500);
}

function hideTyping() {
    if (typingInterval) clearInterval(typingInterval);
    if (typingDiv && typingDiv.parentNode) typingDiv.parentNode.removeChild(typingDiv);
    typingDiv = null;
    typingInterval = null;
}

function toggleChatMinimize() {
    const chatWidget = document.getElementById('chat-widget');
    if (!chatMinimized) {
        chatWidget.classList.add('minimized');
        chatMinimized = true;
    } else {
        chatWidget.classList.remove('minimized');
        chatMinimized = false;
    }
}

window.onload = function() {
    document.getElementById('chat-send').onclick = sendMessage;
    document.getElementById('chat-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    document.getElementById('chat-minimize').onclick = toggleChatMinimize;
    // Minimize chat on first load
    document.getElementById('chat-widget').classList.add('minimized');
};
