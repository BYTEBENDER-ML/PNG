# 🤖 Engagement Regulation Chatbot

A comprehensive chatbot system designed to regulate and monitor user engagement on websites and applications. This system helps users maintain healthy digital habits by providing smart interventions, break reminders, and usage analytics.

## 🌟 Features

### Core Functionality
- **Real-time Engagement Monitoring**: Tracks user activity, session duration, and interaction patterns
- **Smart Interventions**: Automatically suggests breaks and healthy usage patterns
- **Personalized Recommendations**: Provides tailored suggestions based on user behavior
- **Usage Analytics**: Comprehensive reporting on engagement metrics
- **Break Management**: Encourages regular breaks to prevent digital fatigue

### Engagement Rules
The system includes several built-in rules for engagement regulation:

1. **Break Reminder**: Suggests breaks after 1 hour of continuous usage
2. **Excessive Usage Warning**: Alerts users after 4+ hours of total daily usage
3. **Low Engagement Detection**: Identifies when users are distracted or unfocused
4. **Rapid Navigation Detection**: Detects when users are quickly switching between pages

### Chat Interface
- Natural language interaction with the engagement assistant
- Keyword-based responses for common requests
- Real-time engagement score updates
- Session management and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Flask web framework

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web interface**:
   ```bash
   python engagement_web_interface.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
├── chatbot.py                    # Main chatbot logic and engagement regulation
├── engagement_web_interface.py   # Flask web server
├── templates/
│   └── index.html               # Web interface template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── engagement_data.db           # SQLite database (created automatically)
```

## 🔧 Usage

### Basic Usage

1. **Start a Session**: The system automatically starts tracking when you visit the web interface
2. **Monitor Activity**: Your engagement score and session metrics are displayed in real-time
3. **Chat with Assistant**: Use the chat interface to ask questions or request features
4. **Take Breaks**: Click "Take a Break" when you need to step away
5. **View Analytics**: Get detailed insights about your usage patterns

### API Endpoints

The system provides several REST API endpoints:

- `POST /api/activity` - Update user activity
- `POST /api/chat` - Send chat messages
- `GET /api/analytics` - Get engagement analytics
- `POST /api/break` - Take a break
- `POST /api/end-session` - End current session

### Integration with Existing Websites

To integrate this chatbot with your existing website:

1. **Include the tracking script**:
   ```javascript
   // Add this to your website's JavaScript
   function updateEngagement(action, page) {
       fetch('/api/activity', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ action: action, page: page })
       });
   }
   ```

2. **Track user interactions**:
   ```javascript
   // Track clicks
   document.addEventListener('click', () => {
       updateEngagement('click', window.location.pathname);
   });
   
   // Track page views
   updateEngagement('page_view', window.location.pathname);
   ```

3. **Display interventions**:
   ```javascript
   // Check for interventions
   fetch('/api/activity', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ action: 'check', page: window.location.pathname })
   })
   .then(response => response.json())
   .then(data => {
       if (data.interventions) {
           // Display intervention messages to user
           showInterventions(data.interventions);
       }
   });
   ```

## 🎯 Key Features Explained

### Engagement Score Calculation
The system calculates engagement scores based on:
- Interaction frequency (clicks, page views)
- Session duration
- Break patterns
- Focus indicators

### Smart Interventions
The chatbot provides contextual interventions:
- **Break suggestions** with specific activities
- **Focus reminders** when users are distracted
- **Usage warnings** for excessive screen time
- **Engagement boosters** for low-activity periods

### Analytics Dashboard
Comprehensive analytics include:
- Total session time
- Average engagement scores
- Break frequency
- Interaction patterns
- Session history

## 🔒 Privacy & Data

- All data is stored locally in SQLite database
- No external data transmission
- User sessions are anonymous by default
- Data can be easily exported or deleted

## 🛠️ Customization

### Adding New Engagement Rules

You can add custom engagement rules by modifying the `_load_default_rules()` method in `chatbot.py`:

```python
EngagementRule(
    rule_id="custom_rule",
    name="Custom Rule",
    condition="your_condition_here",
    action="your_action_here",
    threshold=your_threshold,
    cooldown=your_cooldown,
    enabled=True
)
```

### Modifying Intervention Messages

Customize intervention messages in the `_create_intervention()` method:

```python
"custom_rule": {
    "type": "custom_intervention",
    "message": "Your custom message",
    "suggestions": ["Suggestion 1", "Suggestion 2"],
    "priority": "medium"
}
```

### Adjusting Thresholds

Modify engagement thresholds in the `EngagementRegulator` class:
- `break_reminder_interval`: Time before suggesting breaks (default: 1 hour)
- `max_session_duration`: Maximum recommended session length (default: 2 hours)
- `engagement_threshold`: Minimum engagement score (default: 0.7)

## 🧪 Testing

Run the included test script:
```bash
python chatbot.py
```

This will demonstrate the chatbot's functionality with example user interactions.

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new engagement rules
- Improving the UI/UX
- Adding new analytics features
- Enhancing the chat interface
- Adding support for different databases

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure the database file has write permissions
4. Check that the Flask server is running on the correct port

## 🔮 Future Enhancements

Potential improvements for future versions:
- Machine learning-based engagement prediction
- Integration with calendar apps for break scheduling
- Mobile app companion
- Team/group engagement analytics
- Integration with productivity tools
- Gamification elements for engagement improvement
