document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('healthChart').getContext('2d');
    
    const healthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Blood Pressure (Systolic)',
                data: [120, 122, 125, 118, 121, 120],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Heart Rate',
                data: [72, 75, 73, 70, 74, 71],
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Handle health data form submission
    const healthDataForm = document.getElementById('healthDataForm');
    healthDataForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(healthDataForm);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/health-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            // Update risk score
            const riskScoreElement = document.querySelector('#riskScore .display-4');
            riskScoreElement.textContent = `${(result.risk_score * 100).toFixed(1)}%`;
            
            // Show success message
            alert('Health data updated successfully!');
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to update health data');
        }
    });
});
