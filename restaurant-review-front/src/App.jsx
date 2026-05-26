import React, { useState } from 'react';

// Gourmet/Restaurant theme with an intense Crimson background
const styles = {
  container: { 
    minHeight: '100vh', 
    backgroundColor: '#721024', // More intense (darker) Crimson background to highlight the app components
    display: 'flex', 
    flexDirection: 'column', 
    alignItems: 'center', 
    justifyContent: 'center', 
    padding: '20px', 
    fontFamily: '"Georgia", "Cambria", serif' // Serif typography mirroring a high-class restaurant menu
  },
  card: { 
    backgroundColor: '#ffffff', 
    padding: '40px 30px', 
    borderRadius: '16px', 
    boxShadow: '0 15px 35px rgba(0, 0, 0, 0.3)', // Enhanced shadow to pop from the dark background
    width: '100%', 
    maxWidth: '500px',
    border: '1px solid #e2b6be',
    boxSizing: 'border-box'
  },
  headerContainer: {
    textAlign: 'center',
    marginBottom: '28px'
  },
  title: { 
    fontSize: '28px', 
    fontWeight: 'bold', 
    color: '#9d1731', // Elegant Crimson for headings
    margin: '0 0 6px 0',
    letterSpacing: '-0.5px'
  },
  subtitle: { 
    fontSize: '14px', 
    color: '#6b5b5d', 
    margin: 0,
    fontFamily: 'system-ui, sans-serif',
    letterSpacing: '0.5px'
  },
  textareaLabel: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '600',
    color: '#4a3b3c',
    marginBottom: '8px',
    fontFamily: 'system-ui, sans-serif'
  },
textarea: { 
    width: '100%', 
    height: '120px', 
    padding: '14px', 
    borderRadius: '8px', 
    border: '2px solid #dc143c', // Distinct Crimson border [cite: 564]
    fontSize: '16px', 
    color: '#2d2122',           
    fontFamily: 'system-ui, sans-serif',
    resize: 'none', 
    marginBottom: '20px', 
    boxSizing: 'border-box',
    outline: 'none',
    backgroundColor: '#fffdfd', 
    transition: 'border-color 0.2s'
  },
  button: { 
    width: '100%', 
    backgroundColor: '#dc143c', // Standard Crimson for the call-to-action button
    color: '#ffffff', 
    padding: '14px', 
    borderRadius: '8px', 
    border: 'none', 
    fontSize: '16px', 
    fontWeight: '600', 
    fontFamily: 'system-ui, sans-serif',
    cursor: 'pointer', 
    boxShadow: '0 4px 12px rgba(220, 20, 60, 0.2)',
    transition: 'all 0.2s'
  },
  error: { 
    color: '#9d1731', 
    backgroundColor: '#fdf2f4', 
    padding: '12px', 
    borderRadius: '8px', 
    marginBottom: '20px', 
    fontSize: '14px',
    fontFamily: 'system-ui, sans-serif',
    border: '1px solid #fbcfe8'
  },
  resultBox: { 
    marginTop: '28px', 
    padding: '20px', 
    borderRadius: '10px', 
    border: '1px solid',
    fontFamily: 'system-ui, sans-serif',
    boxSizing: 'border-box'
  },
  resultTitle: {
    margin: '0 0 12px 0', 
    color: '#2d2122',
    fontSize: '16px',
    fontWeight: '700'
  },
  resultText: {
    margin: '6px 0', 
    color: '#4a3b3c',
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  badge: { 
    display: 'inline-block', 
    padding: '4px 10px', 
    borderRadius: '20px', 
    fontSize: '12px', 
    fontWeight: '700', 
    textTransform: 'uppercase',
    color: '#ffffff'
  }
};

export default function App() {
  const [review, setReview] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const analyzeSentiment = async () => {
    if (!review.trim()) {
      setError('Please enter a valid review before analyzing.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8080/api/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review_text: review })
      });

      const json = await response.json();

      if (response.ok && json.status === 'success') {
        setResult(json.data);
      } else {
        setError(json.error || 'An error occurred while processing the request.');
      }
    } catch (err) {
      setError('Could not connect to Go Gateway. Please check if your Docker containers are active.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.headerContainer}>
          <h1 style={styles.title}>The Bistro Critic</h1>
          <p style={styles.subtitle}>Hybrid Sentiment Analysis Engine (Go + Python)</p>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        <label style={styles.textareaLabel}>Customer Review Text (STR)</label>
        <textarea
          style={styles.textarea}
          placeholder="Describe your dining experience here (e.g., The pasta was perfect but the service was slow)..."
          value={review}
          onChange={(e) => setReview(e.target.value)}
          disabled={loading}
        />

        <button 
          style={{
            ...styles.button, 
            backgroundColor: loading ? '#e27386' : '#dc143c',
            cursor: loading ? 'not-allowed' : 'pointer'
          }} 
          onClick={analyzeSentiment}
          disabled={loading}
        >
          {loading ? 'Consulting the Chef (AI)...' : 'Analyze Culinary Review'}
        </button>

        {result && (
          <div style={{
            ...styles.resultBox, 
            backgroundColor: result.sentiment === 'Positive' ? '#f0fdf4' : '#fff5f5',
            borderColor: result.sentiment === 'Positive' ? '#bbf7d0' : '#ffd1d1'
          }}>
            <h3 style={styles.resultTitle}>Gourmet Intelligence Verdict:</h3>
            <p style={styles.resultText}>
              <strong>Sentiment:</strong>{' '}
              <span style={{
                ...styles.badge,
                backgroundColor: result.sentiment === 'Positive' ? '#15803d' : '#dc143c'
              }}>{result.sentiment}</span>
            </p>
            <p style={{ ...styles.resultText, fontSize: '14px', marginTop: '10px' }}>
              <strong>Model Confidence:</strong> {(result.confidence * 100).toFixed(2)}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
}