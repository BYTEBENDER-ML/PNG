from flask import Flask, render_template, request, jsonify, sessionfrom chatbot import EngagementChatbot
import uuid
import json
import os
from datetime import datetime
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Production configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production'),
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hour
)

# Initialize the chatbot with environment-specific database path
db_path = os.environ.get('DATABASE_PATH', 'engagement_data.db')
chatbot = EngagementChatbot()

@app.route('/')
def index():
    """Main page with engagement monitoring"""
    try:
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        
        # Start or resume session
        if session['user_id'] not in chatbot.regulator.active_sessions:
            chatbot.start_session(session['user_id'], "homepage")
        
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('error.html', error="Failed to load page", code=500), 500

@app.route('/api/activity', methods=['POST'])
def update_activity():
    """Update user activity via API"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({"error": "No user session"}), 400
        
        action = data.get('action', 'page_view')
        page = data.get('page', 'unknown')
        
        result = chatbot.update_activity(user_id, action, page)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error updating activity: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with the engagement assistant"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        message = data.get('message', '')
        
        if not user_id:
            return jsonify({"error": "No user session"}), 400
        
        result = chatbot.chat(user_id, message)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get user engagement analytics"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({"error": "No user session"}), 400
        
        result = chatbot.get_engagement_analytics(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/break', methods=['POST'])
def take_break():
    """User takes a break"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        duration = data.get('duration', 300)  # 5 minutes default
        
        if not user_id:
            return jsonify({"error": "No user session"}), 400
        
        result = chatbot.take_break(user_id, duration)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error taking break: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/end-session', methods=['POST'])
def end_session():
    """End the current session"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({"error": "No user session"}), 400
        
        result = chatbot.end_session(user_id)
        session.pop('user_id', None)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error ending session: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    try:
        active_sessions = len(chatbot.regulator.active_sessions)
        return jsonify({
            "status": "operational",
            "active_sessions": active_sessions,
            "database_path": chatbot.regulator.db_path,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in status check: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Production server configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting engagement chatbot on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Database path: {db_path}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )