// Debounce function to limit how often a function can be called
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

document.addEventListener('DOMContentLoaded', function() {
    const smsForm = document.getElementById('smsForm');
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    // Handle speed selection buttons
    const speedButtons = document.querySelectorAll('.speed-button');
    speedButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            speedButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
        });
    });
    
    // Form submission handler
    if (smsForm) {
        smsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const phoneNumber = document.getElementById('phoneNumber').value;
            const smsCount = document.getElementById('smsCount').value;
            
            // Validate inputs
            if (!phoneNumber || !smsCount) {
                showError('Please fill in all fields');
                return;
            }
            
            // Validate Nepal number format
            if (!/^((98)|(97))\d{8}$/.test(phoneNumber)) {
                showError('Please enter a valid Nepal number (98XXXXXXXX or 97XXXXXXXX)');
                return;
            }
            
            // Validate SMS count
            const count = parseInt(smsCount);
            if (count < 1 || count > 200) {
                showError('SMS count must be between 1 and 200');
                return;
            }
            
            // Show loading state
            showLoading();
            
            // Prepare data for API call
            const data = {
                phone: phoneNumber,
                count: count
            };
            
            // Make API call
            sendSmsRequest(data);
        });
    }
    
    // Function to send SMS request
    function sendSmsRequest(data) {
        // Show progress bar
        progressBar.classList.remove('hidden');
        updateProgress(0);
        
        // Disable form during submission
        disableForm(true);
        
        // Show stop button
        stopBtn.classList.remove('hidden');
        
        fetch('/send_sms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                showResults(data);
            } else {
                showError(data.message || 'An error occurred while sending SMS');
            }
        })
        .catch(error => {
            hideLoading();
            showError('Network error: ' + error.message);
        })
        .finally(() => {
            disableForm(false);
            stopBtn.classList.add('hidden');
            progressBar.classList.add('hidden');
        });
    }
    
    // Stop button handler
    if (stopBtn) {
        stopBtn.addEventListener('click', function() {
            // In a real implementation, you would cancel the request here
            hideLoading();
            disableForm(false);
            stopBtn.classList.add('hidden');
            progressBar.classList.add('hidden');
            showResults({
                success: true,
                results: ['Sending stopped by user'],
                successes: 0,
                total: 0
            });
        });
    }
    
    // Show loading indicator
    function showLoading() {
        loadingIndicator.classList.remove('hidden');
        resultSection.classList.add('hidden');
    }
    
    // Hide loading indicator
    function hideLoading() {
        loadingIndicator.classList.add('hidden');
    }
    
    // Show error message
    function showError(message) {
        resultSection.classList.remove('hidden');
        resultContent.innerHTML = `
            <div class="flex items-center p-3 sm:p-4 bg-red-50 rounded-lg">
                <div class="flex-shrink-0">
                    <i class="fas fa-exclamation-circle text-red-500 text-lg sm:text-xl"></i>
                </div>
                <div class="ml-2 sm:ml-3">
                    <p class="text-red-700 font-medium text-sm sm:text-base">Error</p>
                    <p class="text-red-600 text-sm">${message}</p>
                </div>
            </div>
        `;
        hideLoading();
    }
    
    // Show results
    function showResults(data) {
        resultSection.classList.remove('hidden');
        
        if (data.success) {
            const successRate = data.total > 0 ? Math.round((data.successes / data.total) * 100) : 0;
            
            resultContent.innerHTML = `
                <div class="space-y-3 sm:space-y-4">
                    <div class="flex items-center p-3 sm:p-4 bg-green-50 rounded-lg">
                        <div class="flex-shrink-0">
                            <i class="fas fa-check-circle text-green-500 text-lg sm:text-xl"></i>
                        </div>
                        <div class="ml-2 sm:ml-3">
                            <p class="text-green-700 font-medium text-sm sm:text-base">SMS Sending Complete</p>
                            <p class="text-green-600 text-xs sm:text-sm">${data.successes} out of ${data.total} messages sent successfully</p>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 mt-3 sm:mt-4">
                        <div class="bg-blue-50 p-3 sm:p-4 rounded-lg text-center">
                            <div class="text-lg sm:text-2xl font-bold text-blue-700">${data.total}</div>
                            <div class="text-xs sm:text-sm text-blue-600">Total SMS</div>
                        </div>
                        <div class="bg-green-50 p-3 sm:p-4 rounded-lg text-center">
                            <div class="text-lg sm:text-2xl font-bold text-green-700">${data.successes}</div>
                            <div class="text-xs sm:text-sm text-green-600">Sent</div>
                        </div>
                        <div class="bg-amber-50 p-3 sm:p-4 rounded-lg text-center">
                            <div class="text-lg sm:text-2xl font-bold text-amber-700">${successRate}%</div>
                            <div class="text-xs sm:text-sm text-amber-600">Success Rate</div>
                        </div>
                    </div>
                    
                    <div class="mt-4 sm:mt-6">
                        <h4 class="font-semibold text-gray-800 mb-2 sm:mb-3 text-sm sm:text-base">Detailed Results:</h4>
                        <div class="bg-gray-50 rounded-lg p-3 sm:p-4 max-h-40 sm:max-h-60 overflow-y-auto">
                            <ul class="space-y-1 sm:space-y-2">
                                ${data.results.map(result => `<li class="text-xs sm:text-sm">${result}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            `;
        } else {
            showError(data.message || 'Failed to send SMS messages');
        }
    }
    
    // Update progress bar
    function updateProgress(percent) {
        progressFill.style.width = percent + '%';
        progressText.textContent = percent + '%';
    }
    
    // Disable/enable form
    function disableForm(disable) {
        const inputs = smsForm.querySelectorAll('input, select, button');
        inputs.forEach(input => {
            if (disable) {
                input.setAttribute('disabled', 'disabled');
            } else {
                input.removeAttribute('disabled');
            }
        });
        
        if (disable) {
            startBtn.innerHTML = '<span class="flex items-center justify-center"><i class="fas fa-spinner fa-spin mr-2"></i> SENDING...</span>';
        } else {
            startBtn.innerHTML = '<span class="flex items-center justify-center"><i class="fas fa-paper-plane mr-2"></i> START SENDING</span>';
        }
    }
    
    // Handle window resize with debounce
    const handleResize = debounce(function() {
        // Adjust any responsive elements if needed
    }, 250);
    
    window.addEventListener('resize', handleResize);
    
    // Smooth scroll for anchor links
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
});