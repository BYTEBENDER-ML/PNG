from flask import Flask, render_template, request, jsonify, session
from chatbot import EngagementChatbot
import uuid
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize the chatbot
chatbot = EngagementChatbot()

@app.route('/')
def index():
    """Main page with engagement monitoring"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    # Start or resume session
    if session['user_id'] not in chatbot.regulator.active_sessions:
        chatbot.start_session(session['user_id'], "homepage")
    
    return render_template('index.html')

@app.route('/api/activity', methods=['POST'])
def update_activity():
    """Update user activity via API"""
    data = request.get_json()
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "No user session"}), 400
    
    action = data.get('action', 'page_view')
    page = data.get('page', 'unknown')
    
    result = chatbot.update_activity(user_id, action, page)
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with the engagement assistant"""
    data = request.get_json()
    user_id = session.get('user_id')
    message = data.get('message', '')
    
    if not user_id:
        return jsonify({"error": "No user session"}), 400
    
    result = chatbot.chat(user_id, message)
    return jsonify(result)

@app.route('/api/analytics')
def get_analytics():
    """Get user engagement analytics"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "No user session"}), 400
    
    result = chatbot.get_engagement_analytics(user_id)
    return jsonify(result)

@app.route('/api/break', methods=['POST'])
def take_break():
    """User takes a break"""
    data = request.get_json()
    user_id = session.get('user_id')
    duration = data.get('duration', 300)  # 5 minutes default
    
    if not user_id:
        return jsonify({"error": "No user session"}), 400
    
    result = chatbot.take_break(user_id, duration)
    return jsonify(result)

@app.route('/api/end-session', methods=['POST'])
def end_session():
    """End the current session"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "No user session"}), 400
    
    result = chatbot.end_session(user_id)
    session.pop('user_id', None)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
