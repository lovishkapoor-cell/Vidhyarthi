document.addEventListener('DOMContentLoaded', () => {
    
    // --- Navigation & Sidebar ---
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const navLinks = document.querySelectorAll('.nav-links a');
    const views = document.querySelectorAll('.view-section');

    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');

            // Hide all views
            views.forEach(v => v.classList.remove('active-view'));
            
            // Show target view
            const targetId = link.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active-view');
        });
    });

    // --- Quick Registration Form ---
    const quickRegisterForm = document.getElementById('quickRegisterForm');
    const regStatus = document.getElementById('regStatus');

    if (quickRegisterForm) {
        quickRegisterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('regEmail').value;
            const eventId = document.getElementById('regEventId').value;

            regStatus.textContent = "Registering...";
            regStatus.style.color = "var(--text-muted)";

            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, event_id: eventId })
                });

                const data = await response.json();

                if (response.ok) {
                    regStatus.textContent = "Successfully registered!";
                    regStatus.style.color = "var(--primary-accent)";
                    quickRegisterForm.reset();
                } else {
                    regStatus.textContent = data.detail || "Registration failed.";
                    regStatus.style.color = "red";
                }
            } catch (error) {
                regStatus.textContent = "Network error occurred.";
                regStatus.style.color = "red";
            }
        });
    }

    // --- Zen Zone: Pomodoro Timer ---
    const timerDisplay = document.getElementById('timerDisplay');
    const startBtn = document.getElementById('startTimer');
    const resetBtn = document.getElementById('resetTimer');
    const pomodoroCircle = document.querySelector('.pomodoro-circle');
    
    let timerInterval;
    let isRunning = false;
    const DEFAULT_TIME = 25 * 60; // 25 minutes in seconds
    let timeLeft = DEFAULT_TIME;

    function updateDisplay(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        timerDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    startBtn.addEventListener('click', () => {
        if (!isRunning) {
            isRunning = true;
            startBtn.textContent = "Pause";
            pomodoroCircle.classList.add('running');
            
            timerInterval = setInterval(() => {
                timeLeft--;
                updateDisplay(timeLeft);
                
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    isRunning = false;
                    startBtn.textContent = "Start Focus";
                    pomodoroCircle.classList.remove('running');
                    timeLeft = DEFAULT_TIME;
                    updateDisplay(timeLeft);
                    alert("Focus session complete. Take a break!");
                }
            }, 1000);
        } else {
            isRunning = false;
            startBtn.textContent = "Start Focus";
            pomodoroCircle.classList.remove('running');
            clearInterval(timerInterval);
        }
    });

    resetBtn.addEventListener('click', () => {
        isRunning = false;
        clearInterval(timerInterval);
        startBtn.textContent = "Start Focus";
        pomodoroCircle.classList.remove('running');
        timeLeft = DEFAULT_TIME;
        updateDisplay(timeLeft);
    });

    // --- Floating Chat Widget ---
    const chatWidget = document.getElementById('chatWidget');
    const floatingChatIcon = document.getElementById('floatingChatIcon');
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    const chatBody = document.getElementById('chatBody');
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');

    function toggleChat() {
        chatWidget.classList.toggle('closed');
        if (!chatWidget.classList.contains('closed')) {
            chatInput.focus();
        }
    }

    floatingChatIcon.addEventListener('click', toggleChat);
    chatToggleBtn.addEventListener('click', toggleChat);

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chat-message');
        msgDiv.classList.add(isUser ? 'user-msg' : 'ai-msg');
        msgDiv.textContent = text;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll
    }

    async function handleChatSubmit() {
        const text = chatInput.value.trim();
        if (!text) return;

        // User message
        addMessage(text, true);
        chatInput.value = '';

        // Mock typing indicator
        const typingId = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('chat-message', 'ai-msg', 'muted-text');
        typingDiv.id = typingId;
        typingDiv.textContent = "HubBot is thinking...";
        chatBody.appendChild(typingDiv);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            
            // Remove typing indicator
            document.getElementById(typingId).remove();
            
            // AI response
            addMessage(data.text);

            // Handle AI Tool Calls (Navigation mock)
            if (data.tool_call) {
                setTimeout(() => {
                    if (data.tool_call.name === "navigate_to_page") {
                        const targetPage = data.tool_call.arguments.page_name.toLowerCase();
                        if (targetPage.includes("zen")) {
                            document.querySelector('[data-target="zen-view"]').click();
                        } else if (targetPage.includes("dash")) {
                            document.querySelector('[data-target="dashboard-view"]').click();
                        }
                    }
                }, 1000);
            }

        } catch (error) {
            document.getElementById(typingId).remove();
            addMessage("Oops. Connection to HubBot lost.");
        }
    }

    sendChatBtn.addEventListener('click', handleChatSubmit);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleChatSubmit();
    });

});
