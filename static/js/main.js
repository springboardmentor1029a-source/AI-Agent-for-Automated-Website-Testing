// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission handler
document.getElementById('testForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        websiteUrl: document.getElementById('websiteUrl').value,
        testInstruction: document.getElementById('testInstruction').value,
        browser: document.getElementById('browser').value
    };

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="results-placeholder">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Running tests... Please wait</p>
        </div>
    `;

    try {
        const response = await fetch('/api/run-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="test-result error">
                <h3><i class="fas fa-exclamation-circle"></i> Error</h3>
                <p>Failed to run test: ${error.message}</p>
            </div>
        `;
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    if (data.error) {
        resultsDiv.innerHTML = `
            <div class="test-result error">
                <h3><i class="fas fa-exclamation-circle"></i> Error</h3>
                <p>${data.error}</p>
                ${data.field ? `<p style="color: #666; font-size: 0.9em;">Field: ${data.field}</p>` : ''}
            </div>
        `;
        return;
    }

    let html = `
        <div class="test-result ${data.status === 'success' ? 'success' : 'error'}">
            <h3><i class="fas fa-${data.status === 'success' ? 'check-circle' : 'times-circle'}"></i> Test ${data.status === 'success' ? 'Passed' : 'Failed'}</h3>
            <p><strong>Website:</strong> ${data.websiteUrl}</p>
            <p><strong>Browser:</strong> ${data.browser}</p>
            <p><strong>Test Instruction:</strong> ${data.testInstruction}</p>
            <hr style="margin: 1rem 0; border: none; border-top: 1px solid rgba(0,0,0,0.1);">
            <h4>Results:</h4>
            <div style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.8;">
    `;

    if (data.results && data.results.length > 0) {
        data.results.forEach(result => {
            // Handle multi-line results
            if (result.includes('\n')) {
                html += `<div style="margin-bottom: 0.5rem;">${result.replace(/\n/g, '<br>')}</div>`;
            } else {
                html += `<div style="margin-bottom: 0.5rem;">${result}</div>`;
            }
        });
    } else {
        html += `<div>Test executed successfully</div>`;
    }

    html += `</div>`;

    // Display Validations
    if (data.validations && data.validations.length > 0) {
        html += `
            <div style="margin-top: 1.5rem;">
                <h4><i class="fas fa-check-double"></i> Validations (${data.validations.length}):</h4>
                <div style="margin-left: 1.5rem; margin-top: 0.5rem;">
        `;
        data.validations.forEach(validation => {
            const icon = validation.status === 'pass' ? '✅' : validation.status === 'warning' ? '⚠️' : '❌';
            const color = validation.status === 'pass' ? '#28a745' : validation.status === 'warning' ? '#ffc107' : '#dc3545';
            html += `
                <div style="margin-bottom: 0.5rem; padding: 0.5rem; background: ${validation.status === 'pass' ? '#f0f9ff' : '#fff3cd'}; border-left: 3px solid ${color};">
                    <strong>${icon} ${validation.type}:</strong> ${validation.message}
                </div>
            `;
        });
        html += `</div></div>`;
    }

    // Display Screenshots (filter duplicates)
    if (data.screenshots && data.screenshots.length > 0) {
        // Filter out duplicates and invalid screenshots
        const uniqueScreenshots = [];
        const seenNames = new Set();
        data.screenshots.forEach((screenshot) => {
            if (screenshot && screenshot.base64 && screenshot.name) {
                if (!seenNames.has(screenshot.name)) {
                    seenNames.add(screenshot.name);
                    uniqueScreenshots.push(screenshot);
                }
            }
        });
        
        if (uniqueScreenshots.length > 0) {
            html += `
                <div style="margin-top: 1.5rem;">
                    <h4><i class="fas fa-camera"></i> Screenshots (${uniqueScreenshots.length}):</h4>
                    <div style="margin-top: 0.5rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
            `;
            uniqueScreenshots.forEach((screenshot, index) => {
                const displayName = screenshot.name || `Screenshot ${index + 1}`;
                html += `
                    <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <img src="data:image/png;base64,${screenshot.base64}" 
                             alt="${displayName}" 
                             style="width: 100%; height: auto; display: block; cursor: pointer; transition: transform 0.2s;"
                             onmouseover="this.style.transform='scale(1.02)'"
                             onmouseout="this.style.transform='scale(1)'"
                             onclick="window.open('data:image/png;base64,${screenshot.base64}', '_blank')"
                             title="Click to view full size">
                        <div style="padding: 0.5rem; background: #f8f9fa; font-size: 0.85em; color: #666; text-align: center;">
                            ${displayName}
                        </div>
                    </div>
                `;
            });
            html += `</div></div>`;
        }
    }

    // Display Performance Metrics
    if (data.performance) {
        html += `
            <div style="margin-top: 1.5rem;">
                <h4><i class="fas fa-tachometer-alt"></i> Performance Metrics:</h4>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                    <li>Load Time: ${data.performance.loadTime || 0}ms</li>
                    <li>Page Size: ${data.performance.pageSize || 'N/A'}KB</li>
                </ul>
            </div>
        `;
    }

    html += `</div>`;
    resultsDiv.innerHTML = html;
}

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .workflow-step, .tech-category').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s, transform 0.6s';
    observer.observe(el);
});

