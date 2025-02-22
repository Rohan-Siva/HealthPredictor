document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('diabetesChatForm');
    const chatInput = document.getElementById('diabetesChatInput');
    const chatMessages = document.getElementById('diabetesChatMessages');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        appendMessage('user', message);
        chatInput.value = '';

        try {
            const response = await fetch('/api/diabetes-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            // Add bot response
            appendMessage('bot', data.response);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
        }
    });

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <span class="sender">${sender === 'user' ? 'You' : 'Assistant'}</span>
                <p>${text}</p>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
