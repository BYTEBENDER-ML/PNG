/**
 * Engagement Chatbot Integration Example
 * 
 * This script demonstrates how to integrate the engagement chatbot
 * into any existing website or web application.
 */

class EngagementTracker {
    constructor(apiBaseUrl = '/api') {
        this.apiBaseUrl = apiBaseUrl;
        this.userId = this.getUserId();
        this.sessionStartTime = Date.now();
        this.lastActivityTime = Date.now();
        this.interactionCount = 0;
        this.isTracking = false;
        
        // Initialize tracking
        this.init();
    }
    
    /**
     * Get or create user ID
     */
    getUserId() {
        let userId = localStorage.getItem('engagement_user_id');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('engagement_user_id', userId);
        }
        return userId;
    }
    
    /**
     * Initialize engagement tracking
     */
    init() {
        // Start session
        this.startSession();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start periodic activity updates
        this.startPeriodicUpdates();
        
        this.isTracking = true;
        console.log('Engagement tracking initialized');
    }
    
    /**
     * Start a new session
     */
    async startSession() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/activity`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'session_start',
                    page: window.location.pathname,
                    userId: this.userId
                })
            });
            
            const data = await response.json();
            console.log('Session started:', data);
        } catch (error) {
            console.error('Error starting session:', error);
        }
    }
    
    /**
     * Set up event listeners for user interactions
     */
    setupEventListeners() {
        // Track clicks
        document.addEventListener('click', (e) => {
            this.trackActivity('click', {
                element: e.target.tagName,
                text: e.target.textContent?.substring(0, 50),
                page: window.location.pathname
            });
        });
        
        // Track scroll events
        let scrollTimeout;
        document.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.trackActivity('scroll', {
                    page: window.location.pathname,
                    scrollY: window.scrollY
                });
            }, 100);
        });
        
        // Track form interactions
        document.addEventListener('input', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                this.trackActivity('input', {
                    element: e.target.tagName,
                    page: window.location.pathname
                });
            }
        });
        
        // Track page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.trackActivity('page_hidden', {
                    page: window.location.pathname
                });
            } else {
                this.trackActivity('page_visible', {
                    page: window.location.pathname
                });
            }
        });
        
        // Track page unload
        window.addEventListener('beforeunload', () => {
            this.trackActivity('page_unload', {
                page: window.location.pathname,
                sessionDuration: Date.now() - this.sessionStartTime
            });
        });
    }
    
    /**
     * Start periodic activity updates
     */
    startPeriodicUpdates() {
        // Update activity every 30 seconds
        setInterval(() => {
            this.trackActivity('active', {
                page: window.location.pathname,
                sessionDuration: Date.now() - this.sessionStartTime
            });
        }, 30000);
        
        // Check for interventions every minute
        setInterval(() => {
            this.checkInterventions();
        }, 60000);
    }
    
    /**
     * Track user activity
     */
    async trackActivity(action, details = {}) {
        this.interactionCount++;
        this.lastActivityTime = Date.now();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/activity`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: action,
                    page: window.location.pathname,
                    userId: this.userId,
                    details: details,
                    timestamp: Date.now()
                })
            });
            
            const data = await response.json();
            
            // Update engagement score if provided
            if (data.engagement_score !== undefined) {
                this.updateEngagementDisplay(data.engagement_score);
            }
            
            // Show interventions if any
            if (data.interventions && data.interventions.length > 0) {
                this.showInterventions(data.interventions);
            }
            
        } catch (error) {
            console.error('Error tracking activity:', error);
        }
    }
    
    /**
     * Check for interventions
     */
    async checkInterventions() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/activity`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'check_interventions',
                    page: window.location.pathname,
                    userId: this.userId
                })
            });
            
            const data = await response.json();
            
            if (data.interventions && data.interventions.length > 0) {
                this.showInterventions(data.interventions);
            }
            
        } catch (error) {
            console.error('Error checking interventions:', error);
        }
    }
    
    /**
     * Show intervention messages to user
     */
    showInterventions(interventions) {
        interventions.forEach(intervention => {
            this.showNotification(intervention);
        });
    }
    
    /**
     * Show notification to user
     */
    showNotification(intervention) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `engagement-notification ${intervention.priority}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${this.getNotificationColor(intervention.priority)};
            color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            max-width: 300px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.4;
        `;
        
        notification.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 8px;">
                ${intervention.type.replace('_', ' ').toUpperCase()}
            </div>
            <div style="margin-bottom: 10px;">${intervention.message}</div>
            ${intervention.suggestions ? `
                <div style="font-size: 12px; opacity: 0.9;">
                    <strong>Suggestions:</strong>
                    <ul style="margin: 5px 0; padding-left: 15px;">
                        ${intervention.suggestions.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            <button onclick="this.parentElement.remove()" style="
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin-top: 10px;
            ">Dismiss</button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }
    
    /**
     * Get notification color based on priority
     */
    getNotificationColor(priority) {
        switch (priority) {
            case 'high': return '#dc3545';
            case 'medium': return '#ffc107';
            case 'low': return '#17a2b8';
            default: return '#6c757d';
        }
    }
    
    /**
     * Update engagement display (if exists)
     */
    updateEngagementDisplay(score) {
        const display = document.getElementById('engagement-score');
        if (display) {
            display.textContent = score.toFixed(2);
        }
    }
    
    /**
     * Take a break
     */
    async takeBreak(duration = 300) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/break`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    duration: duration,
                    userId: this.userId
                })
            });
            
            const data = await response.json();
            console.log('Break started:', data);
            
            // Show break notification
            this.showNotification({
                type: 'break_started',
                message: data.message,
                priority: 'medium'
            });
            
        } catch (error) {
            console.error('Error taking break:', error);
        }
    }
    
    /**
     * Get analytics
     */
    async getAnalytics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics?userId=${this.userId}`);
            const data = await response.json();
            console.log('Analytics:', data);
            return data;
        } catch (error) {
            console.error('Error getting analytics:', error);
            return null;
        }
    }
    
    /**
     * End session
     */
    async endSession() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/end-session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: this.userId
                })
            });
            
            const data = await response.json();
            console.log('Session ended:', data);
            
            this.isTracking = false;
            
        } catch (error) {
            console.error('Error ending session:', error);
        }
    }
}

// Usage Examples

// 1. Basic integration - just add this to your website
const engagementTracker = new EngagementTracker();

// 2. Custom API endpoint
// const engagementTracker = new EngagementTracker('https://your-api.com/api');

// 3. Manual break trigger
function takeBreak() {
    engagementTracker.takeBreak(300); // 5 minutes
}

// 4. Get analytics
async function showAnalytics() {
    const analytics = await engagementTracker.getAnalytics();
    if (analytics) {
        console.log('Your engagement analytics:', analytics);
        // Display analytics in your UI
    }
}

// 5. End session when user leaves
window.addEventListener('beforeunload', () => {
    engagementTracker.endSession();
});

// 6. Add engagement score display to your page
function addEngagementDisplay() {
    const display = document.createElement('div');
    display.id = 'engagement-score';
    display.style.cssText = `
        position: fixed;
        top: 10px;
        left: 10px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-family: Arial, sans-serif;
        font-size: 12px;
        z-index: 1000;
    `;
    display.innerHTML = 'Engagement: <span id="score">0.00</span>';
    document.body.appendChild(display);
}

// Initialize display
addEngagementDisplay();

// Export for use in other scripts
window.EngagementTracker = EngagementTracker;
