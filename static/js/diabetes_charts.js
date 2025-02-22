document.addEventListener('DOMContentLoaded', async function() {
    const ctx = document.getElementById('diabetesChart').getContext('2d');
    let diabetesChart;

    // Fetch diabetes data
    try {
        const response = await fetch('/api/diabetes-history');
        const diabetesData = await response.json();
        
        const labels = diabetesData.map(d => d.timestamp);
        const glucoseData = diabetesData.map(d => d.blood_glucose_level);
        const hba1cData = diabetesData.map(d => d.hba1c_level);
        
        diabetesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Blood Glucose (mg/dL)',
                    data: glucoseData,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'HbA1c Level (%)',
                    data: hba1cData,
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
    } catch (error) {
        console.error('Error fetching diabetes data:', error);
    }

    // Handle diabetes data form submission
    const diabetesDataForm = document.getElementById('diabetesDataForm');
    diabetesDataForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(diabetesDataForm);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/diabetes-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            // Update risk score and details
            const riskScore = result.risk_score * 100;
            const riskScoreElement = document.querySelector('#diabetesRiskScore .display-4');
            const riskLevelElement = document.querySelector('#diabetesRiskScore .risk-level');
            const riskAdviceElement = document.querySelector('#diabetesRiskScore .risk-advice');
            
            riskScoreElement.textContent = `${riskScore.toFixed(1)}%`;
            
            // Set risk level and advice
            let level, advice;
            if (riskScore < 20) {
                level = "Low Risk";
                advice = "Maintain healthy lifestyle";
            } else if (riskScore < 40) {
                level = "Moderate Risk";
                advice = "Consider lifestyle improvements";
            } else if (riskScore < 60) {
                level = "Increased Risk";
                advice = "Consult healthcare provider";
            } else {
                level = "High Risk";
                advice = "Urgent medical attention recommended";
            }
            
            riskLevelElement.textContent = level;
            riskAdviceElement.textContent = advice;
            
            // Refresh chart data
            const historyResponse = await fetch('/api/diabetes-history');
            const newDiabetesData = await historyResponse.json();
            
            diabetesChart.data.labels = newDiabetesData.map(d => d.timestamp);
            diabetesChart.data.datasets[0].data = newDiabetesData.map(d => d.blood_glucose_level);
            diabetesChart.data.datasets[1].data = newDiabetesData.map(d => d.hba1c_level);
            diabetesChart.update();
            
            // Show success message
            alert('Diabetes data updated successfully!');
            
            // Reset form
            diabetesDataForm.reset();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to update diabetes data');
        }
    });
});
