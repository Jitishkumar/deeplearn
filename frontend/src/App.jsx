import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Pipelines from './pages/Pipelines'
import Analytics from './pages/Analytics'
import Predictions from './pages/Predictions'
import Login from './pages/Login'
import { getToken } from './services/auth'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    // Check if user is authenticated
    const token = getToken()
    setIsAuthenticated(!!token)
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setIsAuthenticated(false)
  }

  if (!isAuthenticated) {
    return (
      <>
        <Toaster position="top-right" />
        <Login onLogin={handleLogin} />
      </>
    )
  }

  return (
    <>
      <Toaster position="top-right" />
      <Router>
        <Layout onLogout={handleLogout}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/pipelines" element={<Pipelines />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </Router>
    </>
  )
}

export default App
