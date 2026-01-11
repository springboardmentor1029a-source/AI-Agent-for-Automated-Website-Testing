
const Dashboard = {
    stats: {},
    tests: [],
    charts: {},
    
    // Initialize dashboard
    init: function() {
        console.log('🚀 Initializing Dashboard...');
        this.loadStats();
        this.loadRecentTests();
        this.setupEventListeners();
        this.startAutoRefresh();
        console.log('✅ Dashboard initialized');
    },
    
    // Load statistics
    loadStats: async function() {
        try {
            const response = await fetch('/api/statistics');
            const data = await response.json();
            
            if (data.success) {
                this.stats = data.statistics;
                this.updateStatsDisplay();
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            this.showNotification('Failed to load statistics', 'error');
        }
    },
    
    // Load recent tests
    loadRecentTests: async function() {
        try {
            const response = await fetch('/api/reports?limit=10');
            const data = await response.json();
            
            if (data.success) {
                this.tests = data.reports;
                this.updateTestsTable();
            }
        } catch (error) {
            console.error('Error loading tests:', error);
            this.showNotification('Failed to load test history', 'error');
        }
    },
    
    // Update statistics display
    updateStatsDisplay: function() {
        const stats = this.stats;
        
        // Update stat cards
        this.updateElement('#total-tests', stats.total_tests || 0);
        this.updateElement('#passed-tests', stats.passed_tests || 0);
        this.updateElement('#failed-tests', stats.failed_tests || 0);
        this.updateElement('#success-rate', `${(stats.success_rate || 0).toFixed(1)}%`);
        this.updateElement('#avg-time', `${(stats.average_execution_time || 0).toFixed(2)}s`);
        
        // Update progress bar
        const successRate = stats.success_rate || 0;
        const progressBar = document.querySelector('.progress-fill');
        if (progressBar) {
            progressBar.style.width = `${successRate}%`;
        }
    },
    
    // Update tests table
    updateTestsTable: function() {
        const tbody = document.querySelector('#tests-table tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (this.tests.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="no-data">No tests found</td>
                </tr>
            `;
            return;
        }
        
        this.tests.forEach(test => {
            const row = this.createTestRow(test);
            tbody.appendChild(row);
        });
    },
    
    // Create test row
    createTestRow: function(test) {
        const tr = document.createElement('tr');
        tr.className = 'fade-in';
        
        const statusClass = test.success ? 'passed' : 'failed';
        const statusText = test.success ? '✅ Passed' : '❌ Failed';
        
        tr.innerHTML = `
            <td>${test.test_id || 'N/A'}</td>
            <td>
                <span class="status-badge ${statusClass}">${statusText}</span>
            </td>
            <td>${this.formatDate(test.timestamp)}</td>
            <td>${(test.execution_time || 0).toFixed(2)}s</td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="Dashboard.viewReport('${test.test_id}')">
                    View Report
                </button>
            </td>
        `;
        
        return tr;
    },
    
    // View test report
    viewReport: function(testId) {
        window.location.href = `/report/${testId}`;
    },
    
    // Run new test
    runNewTest: async function() {
        const instruction = document.getElementById('test-instruction')?.value;
        const targetUrl = document.getElementById('target-url')?.value;
        
        if (!instruction || !targetUrl) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    instruction: instruction,
                    target_url: targetUrl
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('Test completed successfully!', 'success');
                this.loadStats();
                this.loadRecentTests();
                
                // Redirect to report
                if (data.test_id) {
                    setTimeout(() => {
                        this.viewReport(data.test_id);
                    }, 1000);
                }
            } else {
                this.showNotification(`Test failed: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Error running test:', error);
            this.showNotification('Failed to run test', 'error');
        } finally {
            this.showLoading(false);
        }
    },
    
    // Setup event listeners
    setupEventListeners: function() {
        // Run test button
        const runTestBtn = document.getElementById('run-test-btn');
        if (runTestBtn) {
            runTestBtn.addEventListener('click', () => this.runNewTest());
        }
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refresh());
        }
        
        // Clear history button
        const clearBtn = document.getElementById('clear-history-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearHistory());
        }
    },
    
    // Refresh dashboard
    refresh: function() {
        console.log('🔄 Refreshing dashboard...');
        this.loadStats();
        this.loadRecentTests();
        this.showNotification('Dashboard refreshed', 'success');
    },
    
    // Clear test history
    clearHistory: async function() {
        if (!confirm('Are you sure you want to clear test history?')) {
            return;
        }
        
        try {
            const response = await fetch('/api/clear-history', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('History cleared successfully', 'success');
                this.refresh();
            } else {
                this.showNotification('Failed to clear history', 'error');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            this.showNotification('Failed to clear history', 'error');
        }
    },
    
    // Auto refresh
    startAutoRefresh: function() {
        // Refresh every 30 seconds
        setInterval(() => {
            this.loadStats();
            this.loadRecentTests();
        }, 30000);
    },
    
    // Show loading state
    showLoading: function(show) {
        const loader = document.getElementById('loading-spinner');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
        
        // Disable buttons
        const buttons = document.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.disabled = show;
        });
    },
    
    // Show notification
    showNotification: function(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelectorAll('.notification');
        existing.forEach(n => n.remove());
        
        // Create notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification fade-in`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        notification.innerHTML = `
            <strong>${type.toUpperCase()}:</strong> ${message}
            <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.2em; cursor: pointer;">&times;</button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    },
    
    // Update element text
    updateElement: function(selector, value) {
        const element = document.querySelector(selector);
        if (element) {
            element.textContent = value;
        }
    },
    
    // Format date
    formatDate: function(timestamp) {
        if (!timestamp) return 'N/A';
        
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            
            // Less than 1 minute
            if (diff < 60000) {
                return 'Just now';
            }
            
            // Less than 1 hour
            if (diff < 3600000) {
                const minutes = Math.floor(diff / 60000);
                return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
            }
            
            // Less than 24 hours
            if (diff < 86400000) {
                const hours = Math.floor(diff / 3600000);
                return `${hours} hour${hours > 1 ? 's' : ''} ago`;
            }
            
            // Format as date
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
        } catch (error) {
            return timestamp;
        }
    },
    
    // Export data
    exportData: function() {
        const data = {
            stats: this.stats,
            tests: this.tests,
            exported_at: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `dashboard_export_${Date.now()}.json`;
        a.click();
        
        this.showNotification('Data exported successfully', 'success');
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    Dashboard.init();
});

// Expose Dashboard globally
window.Dashboard = Dashboard;