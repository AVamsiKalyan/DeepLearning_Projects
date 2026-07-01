import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0]
    if (file) {
      // Validate file type
      if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        setError('Please upload a valid image file (JPEG or PNG)')
        return
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }

      setSelectedFile(file)
      setError(null)
      setResult(null)

      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreview(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    e.currentTarget.classList.add('dragover')
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    e.currentTarget.classList.remove('dragover')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    e.currentTarget.classList.remove('dragover')
    
    const file = e.dataTransfer.files?.[0]
    if (file) {
      const changeEvent = {
        target: { files: [file] }
      }
      handleFileSelect(changeEvent)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (err) {
      if (err.response?.status === 503) {
        setError('Server error: Model is not loaded. Please check the backend.')
      } else if (err.response?.status === 400) {
        setError(err.response.data?.detail || 'Invalid file. Please upload a valid image.')
      } else {
        setError(err.response?.data?.detail || 'Failed to analyze image. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreview(null)
    setResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const getPredictionColor = (label) => {
    return label === 'Pneumonia' ? '#ef4444' : '#10b981'
  }

  const getPredictionIcon = (label) => {
    return label === 'Pneumonia' ? '⚠️' : '✓'
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <h1>🫁 Pneumonia Detection AI</h1>
          <p>Medical X-Ray Analysis powered by Deep Learning</p>
        </div>
      </header>

      <main className="main-content">
        <div className="content-wrapper">
          {/* Upload Section */}
          <section className="upload-section">
            <h2>Upload Chest X-Ray Image</h2>
            
            <div
              className="dropzone"
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/jpg"
                onChange={handleFileSelect}
                hidden
              />
              
              {preview ? (
                <div className="preview-container">
                  <img src={preview} alt="Preview" className="preview-image" />
                  <p className="file-name">{selectedFile?.name}</p>
                </div>
              ) : (
                <div className="dropzone-content">
                  <div className="upload-icon">📸</div>
                  <h3>Drag and drop your image here</h3>
                  <p>or click to browse files</p>
                  <p className="file-info">Supported formats: JPEG, PNG (Max 10MB)</p>
                </div>
              )}
            </div>

            {error && (
              <div className="error-message">
                <span className="error-icon">❌</span>
                {error}
              </div>
            )}

            <div className="button-group">
              <button
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={!selectedFile || loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span> Analyzing...
                  </>
                ) : (
                  'Analyze Image'
                )}
              </button>
              
              {preview && (
                <button
                  className="btn btn-secondary"
                  onClick={handleReset}
                  disabled={loading}
                >
                  Clear
                </button>
              )}
            </div>
          </section>

          {/* Results Section */}
          {result && (
            <section className="results-section">
              <h2>Analysis Results</h2>
              
              <div
                className={`prediction-card ${result.label === 'Pneumonia' ? 'pneumonia' : 'normal'}`}
              >
                <div className="prediction-icon">
                  {getPredictionIcon(result.label)}
                </div>
                
                <div className="prediction-label">
                  {result.label === 'Pneumonia' ? 'Pneumonia Detected' : 'Normal (No Pneumonia)'}
                </div>
                
                <div className="confidence-display">
                  <div className="confidence-label">Confidence</div>
                  <div className="confidence-value">{result.confidence}%</div>
                  <div
                    className="confidence-bar"
                    style={{
                      width: `${result.confidence}%`,
                      backgroundColor: getPredictionColor(result.label),
                    }}
                  ></div>
                </div>

                <div className="raw-score">
                  <span>Model Score:</span>
                  <span>{result.raw_score}</span>
                </div>

                {result.label === 'Pneumonia' && (
                  <div className="warning-box">
                    ⚠️ <strong>Important:</strong> This is an AI-assisted analysis. 
                    Please consult a qualified radiologist or healthcare professional for 
                    accurate diagnosis and treatment.
                  </div>
                )}
              </div>

              <button className="btn btn-secondary" onClick={handleReset}>
                Analyze Another Image
              </button>
            </section>
          )}

          {/* Info Section */}
          <section className="info-section">
            <h2>About This Tool</h2>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-icon">🤖</div>
                <h3>AI-Powered Analysis</h3>
                <p>Uses a deep learning ResNet50 model trained on thousands of chest X-rays</p>
              </div>
              <div className="info-card">
                <div className="info-icon">🔬</div>
                <h3>Medical Grade</h3>
                <p>Analyzes 224x224 medical imaging data with preprocessing for accuracy</p>
              </div>
              <div className="info-card">
                <div className="info-icon">⚡</div>
                <h3>Instant Results</h3>
                <p>Get analysis results in seconds with confidence scores</p>
              </div>
              <div className="info-card">
                <div className="info-icon">🔒</div>
                <h3>Secure & Private</h3>
                <p>Your images are analyzed server-side and not stored</p>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer className="footer">
        <p>⚕️ <strong>Medical Disclaimer:</strong> This tool is for educational and research purposes only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment.</p>
      </footer>
    </div>
  )
}

export default App
