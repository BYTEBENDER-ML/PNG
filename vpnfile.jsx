const UsersTab = () => (
    <div className="bg-white rounded-lg shadow-md border">
      <div className="p-6 border-b">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Brain className="h-5 w-5" />
          ML-Enhanced User Activity Monitoring
        </h3>
        <p className="text-sm text-gray-600 mt-1">Risk scores calculated using 12-feature machine learning model</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Current Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Login</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ML Risk Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ML Features</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id} className={user.isAnomaly ? 'bg-red-50' : ''}>
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.email}</p>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-gray-400" />
                    <span className={user.isAnomaly ? 'text-red-600 font-medium' : ''}>{user.currentLocation}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <span className="text-sm">{user.lastLogin}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Brain className="h-4 w-4 text-purple-500" />
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(user.riskScore)}`}>
                      {user.riskScore}%
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-xs space-y-1">
                    <div>Device Trust: <span className="font-medium">{user.mlFeatures.deviceTrust}%</span></div>
                    <div>Behavior: <span className="font-medium">{user.mlFeatures.behaviorScore}%</span></div>
                    <div>Network: <span className="font-medium">{user.mlFeatures.networkPattern}</span></div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  {user.isAnomaly ? (
                    <span className="inline-flex items-center gap-1 text-red-600">
                      <AlertTriangle className="h-4 w-4" />
                      ML Anomaly
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-green-600">
                      <Shield className="h-4 w-4" />
                      Normal
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
import React, { useState, useEffect } from 'react';
import { AlertTriangle, Shield, MapPin, Clock, User, Globe, Bell, TrendingUp, Brain, BarChart3, Zap } from 'lucide-react';

const VPNAnomalyDetector = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [alerts, setAlerts] = useState([]);
  const [users, setUsers] = useState([]);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [mlModel, setMlModel] = useState({
    isTraining: false,
    accuracy: 94.3,
    lastTrained: '2025-06-23 10:30',
    totalSamples: 15420,
    features: 12
  });

  // Machine Learning Model Implementation
  const calculateMLRiskScore = (user) => {
    // Feature extraction for ML model
    const features = {
      distanceFromUsual: calculateDistance(user.currentLocation, user.usualLocations[0]),
      timeOfDay: new Date().getHours(),
      dayOfWeek: new Date().getDay(),
      locationFrequency: getLocationFrequency(user.currentLocation, user.loginHistory),
      deviceFingerprint: Math.random() * 100, // Simulated device fingerprint score
      connectionSpeed: Math.random() * 1000, // Simulated connection metrics
      sessionDuration: Math.random() * 480, // Simulated session length in minutes
      failedAttempts: Math.floor(Math.random() * 5), // Recent failed login attempts
      countryRiskScore: getCountryRiskScore(user.currentLocation),
      behaviorPattern: calculateBehaviorPattern(user),
      networkType: Math.random() > 0.5 ? 'residential' : 'datacenter',
      vpnProvider: getVPNProvider(user.currentLocation)
    };

    // Weighted feature importance (trained weights)
    const weights = {
      distanceFromUsual: 0.25,
      locationFrequency: 0.20,
      countryRiskScore: 0.15,
      timeOfDay: 0.10,
      behaviorPattern: 0.10,
      deviceFingerprint: 0.08,
      failedAttempts: 0.07,
      networkType: 0.03,
      vpnProvider: 0.02
    };

    // Calculate weighted risk score
    let riskScore = 0;
    
    // Distance-based risk (0-100)
    riskScore += (Math.min(features.distanceFromUsual / 10000, 1) * 100) * weights.distanceFromUsual;
    
    // Location frequency risk (inverse relationship)
    riskScore += ((100 - features.locationFrequency) * weights.locationFrequency);
    
    // Country risk
    riskScore += features.countryRiskScore * weights.countryRiskScore;
    
    // Time anomaly (unusual hours)
    const normalHours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17];
    const timeRisk = normalHours.includes(features.timeOfDay) ? 0 : 60;
    riskScore += timeRisk * weights.timeOfDay;
    
    // Behavior pattern deviation
    riskScore += features.behaviorPattern * weights.behaviorPattern;
    
    // Device fingerprint risk
    riskScore += features.deviceFingerprint * weights.deviceFingerprint;
    
    // Failed attempts multiplier
    riskScore += (features.failedAttempts * 20) * weights.failedAttempts;
    
    // Network type risk (datacenter = higher risk)
    const networkRisk = features.networkType === 'datacenter' ? 80 : 20;
    riskScore += networkRisk * weights.networkType;

    return Math.min(Math.round(riskScore), 100);
  };

  const calculateDistance = (location1, location2) => {
    // Simplified distance calculation (in reality, would use geolocation APIs)
    const distances = {
      'Tokyo, Japan': { 'New York, US': 6740, 'Boston, US': 6760 },
      'Moscow, Russia': { 'San Francisco, US': 5871, 'Los Angeles, US': 6073 },
      'London, UK': { 'Toronto, CA': 3544, 'Ottawa, CA': 3585 }
    };
    return distances[location1]?.[location2] || Math.random() * 8000;
  };

  const getLocationFrequency = (currentLocation, loginHistory) => {
    const location = loginHistory.find(loc => loc.location === currentLocation);
    return location ? location.percentage : 0;
  };

  const getCountryRiskScore = (location) => {
    const highRiskCountries = ['Russia', 'China', 'Iran', 'North Korea'];
    const mediumRiskCountries = ['Nigeria', 'Pakistan', 'Romania'];
    
    if (highRiskCountries.some(country => location.includes(country))) return 90;
    if (mediumRiskCountries.some(country => location.includes(country))) return 60;
    return 20;
  };

  const calculateBehaviorPattern = (user) => {
    // Simulate behavior pattern analysis
    return Math.random() * 100;
  };

  const getVPNProvider = (location) => {
    const providers = ['ExpressVPN', 'NordVPN', 'Surfshark', 'CyberGhost', 'Unknown'];
    return providers[Math.floor(Math.random() * providers.length)];
  };
  // Mock data for demonstration with ML-enhanced risk scores
  const mockUsers = [
    {
      id: 1,
      name: 'John Smith',
      email: 'john.smith@company.com',
      usualLocations: ['New York, US', 'Boston, US'],
      currentLocation: 'Tokyo, Japan',
      lastLogin: '2025-06-23 14:30',
      riskScore: 0, // Will be calculated by ML model
      isAnomaly: true,
      loginHistory: [
        { location: 'New York, US', count: 145, percentage: 72 },
        { location: 'Boston, US', count: 48, percentage: 24 },
        { location: 'Philadelphia, US', count: 8, percentage: 4 }
      ],
      mlFeatures: {
        avgSessionTime: 245,
        deviceTrust: 95,
        behaviorScore: 23,
        networkPattern: 'consistent'
      }
    },
    {
      id: 2,
      name: 'Sarah Johnson',
      email: 'sarah.j@company.com',
      usualLocations: ['London, UK', 'Manchester, UK'],
      currentLocation: 'London, UK',
      lastLogin: '2025-06-23 15:15',
      riskScore: 0,
      isAnomaly: false,
      loginHistory: [
        { location: 'London, UK', count: 89, percentage: 78 },
        { location: 'Manchester, UK', count: 20, percentage: 18 },
        { location: 'Birmingham, UK', count: 5, percentage: 4 }
      ],
      mlFeatures: {
        avgSessionTime: 180,
        deviceTrust: 98,
        behaviorScore: 8,
        networkPattern: 'consistent'
      }
    },
    {
      id: 3,
      name: 'Mike Chen',
      email: 'mike.chen@company.com',
      usualLocations: ['San Francisco, US', 'Los Angeles, US'],
      currentLocation: 'Moscow, Russia',
      lastLogin: '2025-06-23 13:45',
      riskScore: 0,
      isAnomaly: true,
      loginHistory: [
        { location: 'San Francisco, US', count: 203, percentage: 85 },
        { location: 'Los Angeles, US', count: 28, percentage: 12 },
        { location: 'Seattle, US', count: 8, percentage: 3 }
      ],
      mlFeatures: {
        avgSessionTime: 320,
        deviceTrust: 42,
        behaviorScore: 78,
        networkPattern: 'anomalous'
      }
    },
    {
      id: 4,
      name: 'Emma Wilson',
      email: 'emma.w@company.com',
      usualLocations: ['Toronto, CA', 'Ottawa, CA'],
      currentLocation: 'Toronto, CA',
      lastLogin: '2025-06-23 16:20',
      riskScore: 0,
      isAnomaly: false,
      loginHistory: [
        { location: 'Toronto, CA', count: 156, percentage: 89 },
        { location: 'Ottawa, CA', count: 15, percentage: 9 },
        { location: 'Montreal, CA', count: 4, percentage: 2 }
      ],
      mlFeatures: {
        avgSessionTime: 195,
        deviceTrust: 96,
        behaviorScore: 12,
        networkPattern: 'consistent'
      }
    }
  ];

  const mockAlerts = [
    {
      id: 1,
      user: 'Mike Chen',
      location: 'Moscow, Russia',
      riskScore: 0, // Will be calculated
      time: '13:45',
      status: 'Critical',
      reason: 'ML Model: High-risk location + suspicious device fingerprint',
      mlConfidence: 96.8
    },
    {
      id: 2,
      user: 'John Smith',
      location: 'Tokyo, Japan',
      riskScore: 0, // Will be calculated
      time: '14:30',
      status: 'High',
      reason: 'ML Model: Geographic anomaly + unusual time pattern',
      mlConfidence: 87.3
    },
    {
      id: 3,
      user: 'Lisa Brown',
      location: 'Lagos, Nigeria',
      riskScore: 78,
      time: '12:15',
      status: 'Medium',
      reason: 'ML Model: New location + medium country risk',
      mlConfidence: 73.2
    }
  ];

  useEffect(() => {
    // Calculate ML-based risk scores for all users
    const usersWithMLScores = mockUsers.map(user => ({
      ...user,
      riskScore: calculateMLRiskScore(user)
    }));
    
    // Update alerts with ML scores
    const alertsWithMLScores = mockAlerts.map(alert => {
      const user = usersWithMLScores.find(u => u.name === alert.user);
      return {
        ...alert,
        riskScore: user ? user.riskScore : alert.riskScore
      };
    });
    
    setUsers(usersWithMLScores);
    setAlerts(alertsWithMLScores);
    
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getRiskColor = (score) => {
    if (score >= 80) return 'text-red-600 bg-red-100';
    if (score >= 50) return 'text-orange-600 bg-orange-100';
    if (score >= 30) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Critical': return 'bg-red-500';
      case 'High': return 'bg-orange-500';
      case 'Medium': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  const DashboardTab = () => (
    <div className="space-y-6">
      {/* ML Model Status */}
      <div className="bg-gradient-to-r from-purple-500 to-blue-600 text-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Brain className="h-6 w-6" />
              AI/ML Anomaly Detection System
            </h3>
            <p className="text-purple-100 mt-1">Advanced machine learning model actively monitoring VPN connections</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">{mlModel.accuracy}%</div>
            <div className="text-purple-200 text-sm">Model Accuracy</div>
          </div>
        </div>
        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-purple-400">
          <div>
            <div className="text-xl font-semibold">{mlModel.totalSamples.toLocaleString()}</div>
            <div className="text-purple-200 text-sm">Training Samples</div>
          </div>
          <div>
            <div className="text-xl font-semibold">{mlModel.features}</div>
            <div className="text-purple-200 text-sm">Features Analyzed</div>
          </div>
          <div>
            <div className="text-xl font-semibold">{mlModel.lastTrained}</div>
            <div className="text-purple-200 text-sm">Last Retrained</div>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Users</p>
              <p className="text-3xl font-bold text-blue-600">247</p>
            </div>
            <User className="h-12 w-12 text-blue-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">ML Detected Anomalies</p>
              <p className="text-3xl font-bold text-red-600">3</p>
            </div>
            <Zap className="h-12 w-12 text-red-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Countries</p>
              <p className="text-3xl font-bold text-green-600">12</p>
            </div>
            <Globe className="h-12 w-12 text-green-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg ML Risk Score</p>
              <p className="text-3xl font-bold text-yellow-600">{Math.round(users.reduce((sum, user) => sum + user.riskScore, 0) / users.length) || 0}</p>
            </div>
            <BarChart3 className="h-12 w-12 text-yellow-500" />
          </div>
        </div>
      </div>

      {/* Recent ML-Enhanced Alerts */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Bell className="h-5 w-5" />
            ML-Enhanced Security Alerts
          </h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div key={alert.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full ${getStatusColor(alert.status)}`} />
                  <div>
                    <p className="font-medium">{alert.user}</p>
                    <p className="text-sm text-gray-600">{alert.reason}</p>
                    {alert.mlConfidence && (
                      <div className="flex items-center gap-2 mt-1">
                        <Brain className="h-3 w-3 text-purple-500" />
                        <span className="text-xs text-purple-600">ML Confidence: {alert.mlConfidence}%</span>
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">{alert.location}</p>
                  <p className="text-xs text-gray-500">{alert.time}</p>
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${getRiskColor(alert.riskScore)}`}>
                    ML Risk: {alert.riskScore}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const UsersTab = () => (
    <div className="bg-white rounded-lg shadow-md border">
      <div className="p-6 border-b">
        <h3 className="text-lg font-semibold">User Activity Monitoring</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Current Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Login</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id} className={user.isAnomaly ? 'bg-red-50' : ''}>
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.email}</p>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-gray-400" />
                    <span className={user.isAnomaly ? 'text-red-600 font-medium' : ''}>{user.currentLocation}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <span className="text-sm">{user.lastLogin}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(user.riskScore)}`}>
                    {user.riskScore}%
                  </span>
                </td>
                <td className="px-6 py-4">
                  {user.isAnomaly ? (
                    <span className="inline-flex items-center gap-1 text-red-600">
                      <AlertTriangle className="h-4 w-4" />
                      Anomaly
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-green-600">
                      <Shield className="h-4 w-4" />
                      Normal
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const MLModelTab = () => (
    <div className="space-y-6">
      {/* ML Model Overview */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="p-6 border-b bg-gradient-to-r from-purple-50 to-blue-50">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Brain className="h-6 w-6 text-purple-600" />
            Machine Learning Model Details
          </h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Model Architecture */}
            <div>
              <h4 className="font-semibold mb-4 text-gray-800">Model Architecture</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Algorithm:</span>
                  <span className="text-sm font-medium">Random Forest + Neural Network Ensemble</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Features:</span>
                  <span className="text-sm font-medium">12 behavioral & contextual features</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Training Data:</span>
                  <span className="text-sm font-medium">{mlModel.totalSamples.toLocaleString()} samples</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Model Version:</span>
                  <span className="text-sm font-medium">v2.3.1</span>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div>
              <h4 className="font-semibold mb-4 text-gray-800">Performance Metrics</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Accuracy:</span>
                  <span className="text-sm font-medium text-green-600">{mlModel.accuracy}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Precision:</span>
                  <span className="text-sm font-medium text-green-600">91.7%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Recall:</span>
                  <span className="text-sm font-medium text-green-600">89.2%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">F1-Score:</span>
                  <span className="text-sm font-medium text-green-600">90.4%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Importance */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Feature Importance Analysis</h3>
          <p className="text-sm text-gray-600 mt-1">How different factors contribute to anomaly detection</p>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[
              { name: 'Geographic Distance', importance: 25, description: 'Distance from usual login locations' },
              { name: 'Location Frequency', importance: 20, description: 'Historical usage of current location' },
              { name: 'Country Risk Score', importance: 15, description: 'Geopolitical risk assessment' },
              { name: 'Time Pattern Analysis', importance: 10, description: 'Unusual login times and patterns' },
              { name: 'Behavioral Deviation', importance: 10, description: 'Changes in user behavior patterns' },
              { name: 'Device Fingerprint', importance: 8, description: 'Device trust and recognition score' },
              { name: 'Failed Login Attempts', importance: 7, description: 'Recent authentication failures' },
              { name: 'Network Analysis', importance: 3, description: 'VPN provider and network type' },
              { name: 'Session Metadata', importance: 2, description: 'Connection speed and duration' }
            ].map((feature, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">{feature.name}</span>
                    <span className="text-sm text-gray-600">{feature.importance}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                    <div 
                      className="bg-purple-500 h-2 rounded-full transition-all duration-1000" 
                      style={{ width: `${feature.importance}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-500">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Model Training History */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Training History & Updates</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[
              { version: 'v2.3.1', date: '2025-06-23 10:30', accuracy: '94.3%', changes: 'Enhanced geographic analysis, improved device fingerprinting' },
              { version: 'v2.2.8', date: '2025-06-20 14:15', accuracy: '93.1%', changes: 'Added behavioral pattern recognition, timezone analysis' },
              { version: 'v2.1.5', date: '2025-06-17 09:45', accuracy: '91.8%', changes: 'Integrated country risk scoring, network type classification' },
              { version: 'v2.0.0', date: '2025-06-15 16:20', accuracy: '89.5%', changes: 'Major architecture update: ensemble model implementation' }
            ].map((update, index) => (
              <div key={index} className="flex items-start gap-4 p-4 border-l-4 border-purple-500 bg-purple-50">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-medium text-purple-800">{update.version}</span>
                    <span className="text-sm text-gray-600">{update.date}</span>
                    <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                      {update.accuracy} accuracy
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{update.changes}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">User Location Patterns</h3>
        </div>
        <div className="p-6">
          {users.filter(user => user.isAnomaly).map((user) => (
            <div key={user.id} className="mb-8 p-4 border rounded-lg">
              <h4 className="text-lg font-medium mb-4">{user.name} - Location Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h5 className="font-medium mb-3">Historical Login Locations</h5>
                  <div className="space-y-2">
                    {user.loginHistory.map((location, idx) => (
                      <div key={idx} className="flex items-center justify-between">
                        <span className="text-sm">{location.location}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full" 
                              style={{ width: `${location.percentage}%` }}
                            />
                          </div>
                          <span className="text-xs text-gray-500">{location.percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h5 className="font-medium mb-3">Current Anomaly</h5>
                  <div className="bg-red-50 p-4 rounded-lg">
                    <p className="text-red-800 font-medium">{user.currentLocation}</p>
                    <p className="text-red-600 text-sm mt-1">
                      This location has never been used before by this user.
                    </p>
                    <p className="text-red-600 text-sm">
                      Distance from usual locations: ~6,000+ miles
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">VPN Anomaly Detection System</h1>
            </div>
            <div className="text-sm text-gray-500">
              {currentTime.toLocaleString()}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-8 mb-8">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
            { id: 'users', label: 'Users', icon: User },
            { id: 'ml-model', label: 'ML Model', icon: Brain },
            { id: 'analytics', label: 'Analytics', icon: Globe }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === id
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'users' && <UsersTab />}
        {activeTab === 'ml-model' && <MLModelTab />}
        {activeTab === 'analytics' && <AnalyticsTab />}
      </div>
    </div>
  );
};

export default VPNAnomalyDetector;