import { useState } from 'react'
import './App.css'

function App() {
  const [topic, setTopic] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [logs, setLogs] = useState([])
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [showServerLogs, setShowServerLogs] = useState(false)
  const [serverLogs, setServerLogs] = useState([])

  const steps = [
    'Web Search',
    'Data Analysis',
    'Image Generation',
    'Formatting',
    'PDF Creation',
    'Verification'
  ]

  const addLog = (message) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`])
  }

  const fetchServerLogs = async () => {
    try {
      const response = await fetch('/api/logs?lines=50')
      const data = await response.json()
      setServerLogs(data.logs || [])
    } catch (err) {
      console.error('Failed to fetch server logs:', err)
    }
  }

  const toggleServerLogs = async () => {
    if (!showServerLogs) {
      await fetchServerLogs()
    }
    setShowServerLogs(!showServerLogs)
  }

  const handleGenerate = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic')
      return
    }

    setIsGenerating(true)
    setCurrentStep(0)
    setLogs([])
    setResult(null)
    setError(null)
    addLog('Starting ebook generation...')

    // Simulate progress
    const progressInterval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < steps.length - 1) {
          addLog(`Step ${prev + 1}: ${steps[prev]} completed`)
          return prev + 1
        }
        return prev
      })
    }, 3000)

    // Poll server logs during generation
    const logInterval = setInterval(async () => {
      if (showServerLogs) {
        await fetchServerLogs()
      }
    }, 2000)

    try {
      // Add timeout to fetch
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 600000) // 10 min timeout

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
        signal: controller.signal
      })

      clearTimeout(timeoutId)
      clearInterval(progressInterval)
      clearInterval(logInterval)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || 'Failed to generate ebook')
      }

      const data = await response.json()
      setResult(data)
      setCurrentStep(steps.length)
      addLog('✅ Ebook generated successfully!')
      
      // Fetch final logs
      if (showServerLogs) {
        await fetchServerLogs()
      }
    } catch (err) {
      clearInterval(progressInterval)
      clearInterval(logInterval)
      const errorMessage = err.name === 'AbortError' 
        ? 'Request timed out. The ebook generation is taking longer than expected.'
        : err.message
      setError(errorMessage)
      addLog(`❌ Error: ${errorMessage}`)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1>🤖 AI Ebook Generator</h1>
        <p className="subtitle">Enter a topic and generate a comprehensive PDF ebook</p>

        <div className="input-section">
          <label htmlFor="topic">Topic</label>
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Learn Python from Scratch"
            disabled={isGenerating}
          />
          <button 
            onClick={handleGenerate}
            disabled={isGenerating || !topic.trim()}
            className="generate-btn"
          >
            {isGenerating ? '⏳ Generating...' : '🚀 Generate Ebook'}
          </button>
        </div>

        {(isGenerating || result || error) && (
          <div className="progress-section">
            <h3>Progress</h3>
            <div className="steps">
              {steps.map((step, index) => (
                <div 
                  key={index}
                  className={`step ${
                    index < currentStep ? 'completed' : 
                    index === currentStep ? 'active' : 
                    'pending'
                  }`}
                >
                  <span className="step-icon">
                    {index < currentStep ? '✓' : 
                     index === currentStep ? '►' : 
                     '○'}
                  </span>
                  <span className="step-text">Step {index + 1}: {step}</span>
                </div>
              ))}
            </div>

            <div className="logs">
              <div className="logs-header">
                <h4>Client Logs</h4>
                <button 
                  onClick={toggleServerLogs}
                  className="toggle-logs-btn"
                >
                  {showServerLogs ? '📋 Hide Server Logs' : '📋 Show Server Logs'}
                </button>
              </div>
              <div className="log-content">
                {logs.map((log, index) => (
                  <div key={index} className="log-entry">{log}</div>
                ))}
              </div>
            </div>

            {showServerLogs && (
              <div className="logs server-logs">
                <div className="logs-header">
                  <h4>Server Logs</h4>
                  <button 
                    onClick={fetchServerLogs}
                    className="refresh-logs-btn"
                    disabled={isGenerating}
                  >
                    🔄 Refresh
                  </button>
                </div>
                <div className="log-content">
                  {serverLogs.length > 0 ? (
                    serverLogs.map((log, index) => (
                      <div key={index} className="log-entry server-log">{log}</div>
                    ))
                  ) : (
                    <div className="log-entry">No server logs available</div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {result && (
          <div className="result-section">
            <h3>✨ Success!</h3>
            <p>Your ebook is ready</p>
            <a 
              href={`http://localhost:8000/static/${result.filename}`}
              download={result.filename}
              target="_blank"
              rel="noopener noreferrer"
              className="download-btn"
            >
              📥 Download {result.filename}
            </a>
          </div>
        )}

        {error && (
          <div className="error-section">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
