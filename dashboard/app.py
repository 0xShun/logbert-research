"""
LogBERT Dashboard

A Flask web application for visualizing and interacting with the LogBERT model.
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import numpy as np
from typing import Dict, List

app = Flask(__name__)

# TODO: Import your model and utilities
# from models.logbert import LogBERT
# from utils.tokenize_utils import tokenize_text

class DashboardData:
    """Mock data for dashboard demonstration."""
    
    def __init__(self):
        self.sample_logs = [
            "2024-01-01 10:00:00 INFO User login successful",
            "2024-01-01 10:01:00 ERROR Database connection failed",
            "2024-01-01 10:02:00 WARN High memory usage detected",
            "2024-01-01 10:03:00 INFO File upload completed",
            "2024-01-01 10:04:00 ERROR Authentication failed"
        ]
        
        self.templates = [
            "User login successful",
            "Database connection failed", 
            "High memory usage detected",
            "File upload completed",
            "Authentication failed"
        ]

dashboard_data = DashboardData()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/api/logs')
def get_logs():
    """API endpoint to get sample logs."""
    return jsonify({
        'logs': dashboard_data.sample_logs,
        'templates': dashboard_data.templates
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_log():
    """API endpoint to analyze a log entry."""
    data = request.get_json()
    log_entry = data.get('log_entry', '')
    
    # TODO: Implement actual log analysis
    analysis_result = {
        'template': 'Sample template extracted',
        'anomaly_score': 0.15,
        'confidence': 0.85,
        'suggestions': ['Check system resources', 'Monitor database connections']
    }
    
    return jsonify(analysis_result)

@app.route('/api/templates')
def get_templates():
    """API endpoint to get log templates."""
    return jsonify({
        'templates': dashboard_data.templates,
        'count': len(dashboard_data.templates)
    })

@app.route('/api/stats')
def get_stats():
    """API endpoint to get dashboard statistics."""
    stats = {
        'total_logs': 1000,
        'unique_templates': 50,
        'anomalies_detected': 15,
        'model_accuracy': 0.92
    }
    return jsonify(stats)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create a simple HTML template
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>LogBERT Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }
        .stats { display: flex; justify-content: space-between; }
        .stat-item { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LogBERT Dashboard</h1>
        
        <div class="card">
            <h2>Statistics</h2>
            <div class="stats" id="stats">
                <div class="stat-item">
                    <h3>Total Logs</h3>
                    <p id="total-logs">Loading...</p>
                </div>
                <div class="stat-item">
                    <h3>Unique Templates</h3>
                    <p id="unique-templates">Loading...</p>
                </div>
                <div class="stat-item">
                    <h3>Anomalies Detected</h3>
                    <p id="anomalies">Loading...</p>
                </div>
                <div class="stat-item">
                    <h3>Model Accuracy</h3>
                    <p id="accuracy">Loading...</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Log Analysis</h2>
            <textarea id="log-input" placeholder="Enter log entry here..." rows="4" style="width: 100%;"></textarea>
            <button onclick="analyzeLog()">Analyze</button>
            <div id="analysis-result"></div>
        </div>
        
        <div class="card">
            <h2>Sample Logs</h2>
            <div id="sample-logs"></div>
        </div>
    </div>
    
    <script>
        // Load dashboard data
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-logs').textContent = data.total_logs;
                document.getElementById('unique-templates').textContent = data.unique_templates;
                document.getElementById('anomalies').textContent = data.anomalies_detected;
                document.getElementById('accuracy').textContent = (data.model_accuracy * 100).toFixed(1) + '%';
            });
            
        fetch('/api/logs')
            .then(response => response.json())
            .then(data => {
                const logsDiv = document.getElementById('sample-logs');
                data.logs.forEach(log => {
                    logsDiv.innerHTML += '<p>' + log + '</p>';
                });
            });
            
        function analyzeLog() {
            const logEntry = document.getElementById('log-input').value;
            fetch('/api/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({log_entry: logEntry})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('analysis-result').innerHTML = 
                    '<h3>Analysis Result:</h3>' +
                    '<p><strong>Template:</strong> ' + data.template + '</p>' +
                    '<p><strong>Anomaly Score:</strong> ' + data.anomaly_score + '</p>' +
                    '<p><strong>Confidence:</strong> ' + data.confidence + '</p>';
            });
        }
    </script>
</body>
</html>
    """
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    print("Dashboard initialized successfully!")
    print("Run 'python dashboard/app.py' to start the dashboard")
    print("Then visit http://localhost:5000 in your browser") 