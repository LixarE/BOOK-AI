async function startGeneration() {
    const topic = document.getElementById('topic').value;
    const generateBtn = document.getElementById('generateBtn');
    const statusContainer = document.getElementById('status');
    const resultContainer = document.getElementById('result');
    const logs = document.getElementById('logs');
    const steps = document.getElementById('steps').children;

    if (!topic) {
        alert('Please enter a topic.');
        return;
    }

    generateBtn.disabled = true;
    statusContainer.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    logs.innerText = 'Starting process...';

    // Reset steps
    for (let li of steps) {
        li.className = 'pending';
    }

    try {
        // Simulate steps visually since we don't have real-time sockets yet
        // In a real app, we'd use WebSockets or Server-Sent Events
        let stepIndex = 0;
        const interval = setInterval(() => {
            if (stepIndex < steps.length - 1) { // Don't finish the last one until done
                if (stepIndex > 0) steps[stepIndex - 1].className = 'completed';
                steps[stepIndex].className = 'active';
                logs.innerText += `\nRunning Step ${stepIndex + 1}...`;
                logs.scrollTop = logs.scrollHeight;
                stepIndex++;
            }
        }, 3000); // Fake progress every 3 seconds

        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic })
        });

        clearInterval(interval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate ebook');
        }

        const data = await response.json();

        // Mark all as complete
        for (let li of steps) {
            li.className = 'completed';
        }
        logs.innerText += '\nProcess Completed Successfully!';

        resultContainer.classList.remove('hidden');
        const downloadLink = document.getElementById('downloadLink');
        downloadLink.href = data.pdf_path; // Assuming backend returns relative path
        downloadLink.innerText = `Download ${data.filename}`;

    } catch (error) {
        console.error(error);
        logs.innerText += `\nError: ${error.message}`;
        alert(`Error: ${error.message}`);
    } finally {
        generateBtn.disabled = false;
    }
}
