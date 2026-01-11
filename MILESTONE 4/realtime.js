
const Realtime = {
    updateInterval: null,
    isConnected: false,
    
    // Initialize real-time updates
    init: function() {
        console.log('⚡ Initializing Real-time Updates...');
        this.startPolling();
        this.setupVisibilityHandler();
        console.log('✅ Real-time updates initialized');
    },
    
    // Start polling for updates
    startPolling: function() {
        // Poll every 5 seconds
        this.updateInterval = setInterval(() => {
            this.checkForUpdates();
        }, 5000);
        
        this.isConnected = true;
    },
    
    // Stop polling
    stopPolling: function() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isConnected = false;
    },
    
    // Check for updates
    checkForUpdates: async function() {
        try {
            const response = await fetch('/api/updates');
            const data = await response.json();
            
            if (data.success && data.has_updates) {
                this.handleUpdates(data.updates);
            }
        } catch (error) {
            console.error('Error checking for updates:', error);
        }
    },
    
    // Handle incoming updates
    handleUpdates: function(updates) {
        updates.forEach(update => {
            switch (update.type) {
                case 'new_test':
                    this.handleNewTest(update.data);
                    break;
                case 'test_completed':
                    this.handleTestCompleted(update.data);
                    break;
                case 'test_failed':
                    this.handleTestFailed(update.data);
                    break;
                default:
                    console.log('Unknown update type:', update.type);
            }
        });
        
        // Refresh dashboard
        if (window.Dashboard) {
            Dashboard.refresh();
        }
    },
    
    // Handle new test
    handleNewTest: function(data) {
        console.log('🆕 New test started:', data.test_id);
        
        if (window.Dashboard) {
            Dashboard.showNotification(`New test started: ${data.test_id}`, 'info');
        }
        
        // Show running indicator
        this.showRunningIndicator(data.test_id);
    },
    
    // Handle test completed
    handleTestCompleted: function(data) {
        console.log('✅ Test completed:', data.test_id);
        
        if (window.Dashboard) {
            Dashboard.showNotification(`Test completed: ${data.test_id}`, 'success');
        }
        
        // Remove running indicator
        this.hideRunningIndicator(data.test_id);
        
        // Play success sound
        this.playSound('success');
    },
    
    // Handle test failed
    handleTestFailed: function(data) {
        console.log('❌ Test failed:', data.test_id);
        
        if (window.Dashboard) {
            Dashboard.showNotification(`Test failed: ${data.test_id}`, 'error');
        }
        
        // Remove running indicator
        this.hideRunningIndicator(data.test_id);
        
        // Play error sound
        this.playSound('error');
    },
    
    // Show running indicator
    showRunningIndicator: function(testId) {
        const indicator = document.createElement('div');
        indicator.id = `running-${testId}`;
        indicator.className = 'running-indicator';
        indicator.innerHTML = `
            <div class="loading-spinner"></div>
            <span>Test ${testId} running...</span>
        `;
        indicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 9998;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        
        document.body.appendChild(indicator);
    },
    
    // Hide running indicator
    hideRunningIndicator: function(testId) {
        const indicator = document.getElementById(`running-${testId}`);
        if (indicator) {
            indicator.remove();
        }
    },
    
    // Play notification sound
    playSound: function(type) {
        // Create audio element
        const audio = new Audio();
        
        switch (type) {
            case 'success':
                // Success sound (simple beep)
                audio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBCx+zPDTgDQIF2Sz7uijViQKT3Hn7rlpHwU'; // Placeholder
                break;
            case 'error':
                // Error sound
                audio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBCx+zPDTgDQIF2Sz7uijViQKT3Hn7rlpHwU';
                break;
            default:
                return;
        }
        
        audio.volume = 0.3;
        audio.play().catch(err => console.log('Audio play failed:', err));
    },
    
    // Setup page visibility handler
    setupVisibilityHandler: function() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('Page hidden, stopping polling');
                this.stopPolling();
            } else {
                console.log('Page visible, resuming polling');
                this.startPolling();
            }
        });
    },
    
    // Get connection status
    getStatus: function() {
        return {
            connected: this.isConnected,
            polling: !!this.updateInterval
        };
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    Realtime.init();
});

// Expose Realtime globally
window.Realtime = Realtime;