document.addEventListener('DOMContentLoaded', () => {

    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', handleSend);

    async function handleSend() {

        const scenario = userInput.value.trim();

        if (!scenario) return;

        addMessage(scenario, 'user');

        userInput.value = '';

        try {

            const res = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario })
            });

            const data = await res.json();

            if (data.conversational_response) {

                addMessage(data.conversational_response, 'ai', true);

            }

            if (data.results) {

                renderResults(data.results);

            }

        } catch (err) {

            addMessage("Backend error. Make sure server is running.", 'ai');

        }

    }

    function addMessage(content, sender, isHtml = false) {

        const msg = document.createElement('div');

        msg.className = `message ${sender}-message`;

        const body = document.createElement('div');

        body.className = 'message-content';

        if (isHtml) body.innerHTML = content;
        else body.textContent = content;

        msg.appendChild(body);

        chatContainer.appendChild(msg);

        chatContainer.scrollTop = chatContainer.scrollHeight;

    }

    function renderResults(results) {

        const wrap = document.createElement('div');

        wrap.className = 'legal-results';

        results.forEach(res => {

            const law = res.legal_info;

            const card = document.createElement('div');

            card.className = 'result-card';

            card.innerHTML = `
<div class="card-header">
<span class="section-tag">${law.section}</span>
</div>

<strong>${law.crime}</strong>

<p class="short-desc">${law.description}</p>

<div style="margin-top:6px;font-size:0.8rem;color:#fbbf24">
Punishment: ${law.punishment}
</div>
`;

            wrap.appendChild(card);

        });

        chatContainer.appendChild(wrap);

    }
});