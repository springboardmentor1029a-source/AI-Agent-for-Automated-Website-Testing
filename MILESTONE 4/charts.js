
const Charts = {
    instances: {},
    
    // Initialize all charts
    init: function() {
        console.log('📊 Initializing Charts...');
        this.createSuccessRateChart();
        this.createTestTrendChart();
        this.createExecutionTimeChart();
        console.log('✅ Charts initialized');
    },
    
    // Create success rate chart
    createSuccessRateChart: async function() {
        const canvas = document.getElementById('success-rate-chart');
        if (!canvas) return;
        
        try {
            const data = await this.fetchSuccessRateData();
            
            // Destroy existing chart
            if (this.instances.successRate) {
                this.instances.successRate.destroy();
            }
            
            // Create simple chart (without Chart.js library)
            this.drawSuccessRateChart(canvas, data);
        } catch (error) {
            console.error('Error creating success rate chart:', error);
        }
    },
    
    // Create test trend chart
    createTestTrendChart: async function() {
        const canvas = document.getElementById('test-trend-chart');
        if (!canvas) return;
        
        try {
            const data = await this.fetchTestTrendData();
            this.drawTrendChart(canvas, data);
        } catch (error) {
            console.error('Error creating trend chart:', error);
        }
    },
    
    // Create execution time chart
    createExecutionTimeChart: async function() {
        const canvas = document.getElementById('execution-time-chart');
        if (!canvas) return;
        
        try {
            const data = await this.fetchExecutionTimeData();
            this.drawBarChart(canvas, data);
        } catch (error) {
            console.error('Error creating execution time chart:', error);
        }
    },
    
    // Fetch success rate data
    fetchSuccessRateData: async function() {
        try {
            const response = await fetch('/api/statistics/trend?days=7');
            const data = await response.json();
            
            if (data.success) {
                return data.trend || [];
            }
        } catch (error) {
            console.error('Error fetching success rate data:', error);
        }
        
        return [];
    },
    
    // Fetch test trend data
    fetchTestTrendData: async function() {
        try {
            const response = await fetch('/api/reports?limit=20');
            const data = await response.json();
            
            if (data.success) {
                return data.reports || [];
            }
        } catch (error) {
            console.error('Error fetching trend data:', error);
        }
        
        return [];
    },
    
    // Fetch execution time data
    fetchExecutionTimeData: async function() {
        return await this.fetchTestTrendData();
    },
    
    // Draw success rate chart (donut chart)
    drawSuccessRateChart: function(canvas, data) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) / 2 - 20;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        if (data.length === 0) {
            ctx.fillStyle = '#999';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No data available', centerX, centerY);
            return;
        }
        
        // Calculate totals
        const latest = data[data.length - 1];
        const passed = latest.passed_tests || 0;
        const failed = (latest.total_tests || 0) - passed;
        const total = passed + failed;
        
        if (total === 0) {
            ctx.fillStyle = '#999';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No tests yet', centerX, centerY);
            return;
        }
        
        // Draw donut chart
        const passedAngle = (passed / total) * 2 * Math.PI;
        
        // Draw passed segment
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -Math.PI / 2, -Math.PI / 2 + passedAngle);
        ctx.strokeStyle = '#4caf50';
        ctx.lineWidth = 40;
        ctx.stroke();
        
        // Draw failed segment
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -Math.PI / 2 + passedAngle, 3 * Math.PI / 2);
        ctx.strokeStyle = '#f44336';
        ctx.lineWidth = 40;
        ctx.stroke();
        
        // Draw center text
        ctx.fillStyle = '#333';
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${((passed / total) * 100).toFixed(0)}%`, centerX, centerY);
        
        ctx.font = '14px Arial';
        ctx.fillText(`${passed}/${total} passed`, centerX, centerY + 30);
    },
    
    // Draw trend chart (line chart)
    drawTrendChart: function(canvas, data) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const padding = 40;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        if (data.length === 0) {
            ctx.fillStyle = '#999';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No data available', width / 2, height / 2);
            return;
        }
        
        // Prepare data
        const points = data.slice(-10).map((test, index) => ({
            x: padding + (index / (data.length - 1)) * (width - 2 * padding),
            y: height - padding - (test.success ? (height - 2 * padding) : 0)
        }));
        
        // Draw grid
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = padding + (i / 4) * (height - 2 * padding);
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();
        }
        
        // Draw line
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 3;
        ctx.beginPath();
        points.forEach((point, index) => {
            if (index === 0) {
                ctx.moveTo(point.x, point.y);
            } else {
                ctx.lineTo(point.x, point.y);
            }
        });
        ctx.stroke();
        
        // Draw points
        points.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = '#667eea';
            ctx.fill();
        });
    },
    
    // Draw bar chart
    drawBarChart: function(canvas, data) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const padding = 40;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        if (data.length === 0) {
            ctx.fillStyle = '#999';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No data available', width / 2, height / 2);
            return;
        }
        
        // Prepare data
        const recentTests = data.slice(-10);
        const maxTime = Math.max(...recentTests.map(t => t.execution_time || 0));
        const barWidth = (width - 2 * padding) / recentTests.length - 10;
        
        // Draw bars
        recentTests.forEach((test, index) => {
            const barHeight = ((test.execution_time || 0) / maxTime) * (height - 2 * padding);
            const x = padding + index * (barWidth + 10);
            const y = height - padding - barHeight;
            
            ctx.fillStyle = test.success ? '#4caf50' : '#f44336';
            ctx.fillRect(x, y, barWidth, barHeight);
            
            // Draw time label
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`${(test.execution_time || 0).toFixed(1)}s`, x + barWidth / 2, y - 5);
        });
        
        // Draw x-axis
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();
    },
    
    // Refresh all charts
    refresh: function() {
        console.log('🔄 Refreshing charts...');
        this.createSuccessRateChart();
        this.createTestTrendChart();
        this.createExecutionTimeChart();
    }
};

// Initialize charts on load
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure Dashboard is loaded
    setTimeout(() => {
        Charts.init();
    }, 500);
});

// Expose Charts globally
window.Charts = Charts;