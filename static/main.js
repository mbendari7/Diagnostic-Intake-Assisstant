const intakeForm = document.getElementById('intake-form');
const submitButton = document.getElementById('submit-btn');
const loadingIndicator = document.getElementById('loading-indicator');
const statusPanel = document.getElementById('status-panel');
const diagnosticFeed = document.getElementById('diagnostic-feed');

// New elements for the follow-up feature
const followUpContainer = document.getElementById('follow-up-container');
const followUpForm = document.getElementById('follow-up-form');
const followUpInput = document.getElementById('follow-up-text');
const followUpBtn = document.getElementById('follow-up-btn');

// --- Phase 1: The Initial Hardware Scan ---
intakeForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    submitButton.disabled = true;
    submitButton.innerText = "Processing Scan...";
    statusPanel.style.display = "block";
    loadingIndicator.style.display = "block";

    const formData = new FormData(intakeForm);

    try {
        const serverResponse = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const aiResponseHtml = await serverResponse.text();

        // Inject the master report into the feed
        diagnosticFeed.innerHTML = aiResponseHtml;
        
        // Hide the initial intake form and reveal the follow-up chat box
        document.getElementById('initial-intake-wrapper').style.display = "none";
        followUpContainer.style.display = "block";

    } catch (error) {
        diagnosticFeed.innerHTML = `<div class="error-panel">Connection Error: Ensure app.py is running.</div>`;
    } finally {
        statusPanel.style.display = "none";
    }
});

// --- Phase 2: The Conversational Follow-Up ---
followUpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageText = followUpInput.value;
    if (!messageText) return;

    // 1. Visually add the user's question to the feed immediately
    followUpBtn.disabled = true;
    followUpBtn.innerText = "Thinking...";
    
    const userBubble = document.createElement('div');
    userBubble.className = "user-chat-bubble";
    userBubble.innerHTML = `<strong>You:</strong> ${messageText}`;
    diagnosticFeed.appendChild(userBubble);

    const formData = new FormData(followUpForm);

    try {
        // 2. Send the question to the new /reply endpoint
        const serverResponse = await fetch('/reply', {
            method: 'POST',
            body: formData
        });

        const aiReplyHtml = await serverResponse.text();

        // 3. Append the AI's response to the feed below the user's question
        const aiBubble = document.createElement('div');
        aiBubble.innerHTML = aiReplyHtml;
        diagnosticFeed.appendChild(aiBubble);

        // Auto-scroll to the bottom of the feed
        window.scrollTo(0, document.body.scrollHeight);

    } catch (error) {
        const errorBubble = document.createElement('div');
        errorBubble.className = "error-panel";
        errorBubble.innerText = "Failed to send reply.";
        diagnosticFeed.appendChild(errorBubble);
    } finally {
        followUpBtn.disabled = false;
        followUpBtn.innerText = "Send Reply";
        followUpForm.reset();
    }
});