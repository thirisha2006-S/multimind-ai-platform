import React, { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get('/api/')
      .then((res) => setStatus(res.data))
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <div>Error: {error}</div>
  if (!status) return <div>Loading...</div>

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>{status.name}</h1>
      <p>Version: {status.version}</p>
      <p>Status: {status.status}</p>
      <p>Environment: {status.environment}</p>
    </div>
  )
}

export default App