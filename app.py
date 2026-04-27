from flask import Flask, render_template, request
import json
import google.generativeai as genai
import scanner 

app = Flask(__name__)

# --- My AI Connection Settings ---
MY_SECURE_API_KEY = "YOUR_SECURE_API_KEY_HERE" 
genai.configure(api_key=MY_SECURE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# I create a global chat session variable to remember the conversation locally
active_chat_session = None

@app.route('/')
def home():
    # Every time the page is refreshed, I wipe the memory for a fresh scan
    global active_chat_session
    active_chat_session = model.start_chat(history=[])
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global active_chat_session
    user_complaint = request.form.get('complaint')
    diagnostic_data = scanner.get_live_data()
    
    structured_ai_prompt = f"""
    You are my IT Expert Triage Specialist (Level 3).
    Analyze the following user complaint and the attached local telemetry.
    
    User Complaint: {user_complaint}
    System Telemetry payload: {json.dumps(diagnostic_data)}
    
    *** YOU MUST OUTPUT YOUR ENTIRE RESPONSE AS VALID HTML. DO NOT USE ANY MARKDOWN. ***
    
    Provide the response with the following structured HTML elements:
    1. An Executive Diagnosis in an <h2> heading with id="ai-diagnosis".
    2. A distinct panel for Hardware Analysis in a <div> with class="triage-panel". Include <h3> subheadings.
    3. A distinct panel for Software and Process Analysis in a <div> with class="triage-panel". 
    4. A prioritized troubleshooting plan in an <ol> list.
    5. A 'Helpful Resources' section at the bottom containing 2-3 relevant, real URLs to official support pages or driver downloads. Format these as clickable HTML links (<a href="..." target="_blank">).
    """
    
    try:
        response = active_chat_session.send_message(structured_ai_prompt)
        return f"<div class='ai-report-container'>{response.text}</div>"
    except Exception as e:
        return f"<div class='error-panel'>API Connection Error: {e}</div>"

@app.route('/reply', methods=['POST'])
def reply():
    # This new route handles the follow-up questions
    global active_chat_session
    user_message = request.form.get('message')
    
    follow_up_prompt = f"""
    The user has a follow-up question regarding the current diagnostic session:
    "{user_message}"
    
    *** YOU MUST OUTPUT YOUR ENTIRE RESPONSE AS VALID HTML. DO NOT USE ANY MARKDOWN. ***
    Answer the question directly and professionally. If applicable, provide clickable HTML links to trusted resources or documentation. Keep the response wrapped in a <div class="ai-reply-panel">.
    """
    
    try:
        # Sending this to the active session means the AI remembers the hardware data!
        response = active_chat_session.send_message(follow_up_prompt)
        return response.text
    except Exception as e:
        return f"<div class='error-panel'>API Reply Error: {e}</div>"

if __name__ == '__main__':
    app.run(debug=True)