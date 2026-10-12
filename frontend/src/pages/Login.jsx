import React, { useState } from 'react'
import { login, register } from '../services/auth'
import toast from 'react-hot-toast'

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    fullName: '',
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isRegister) {
        await register(formData.email, formData.username, formData.password, formData.fullName)
        toast.success('Registration successful! Please login.')
        setIsRegister(false)
        setFormData({ username: '', password: '', email: '', fullName: '' })
      } else {
        await login(formData.username, formData.password)
        toast.success('Login successful!')
        onLogin()
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDemoLogin = async () => {
    setLoading(true)
    try {
      await login('demo', 'demo123')
      toast.success('Logged in as demo user!')
      onLogin()
    } catch (error) {
      toast.error('Demo login failed. Please initialize the database first.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🚀 AI DevOps Pipeline</h1>
          <p className="text-blue-100">Intelligent CI/CD with Machine Learning</p>
        </div>

        {/* Login/Register Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {isRegister ? 'Create Account' : 'Welcome Back'}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegister && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="you@example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="John Doe"
                  />
                </div>
              </>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="username"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50"
            >
              {loading ? 'Please wait...' : isRegister ? 'Register' : 'Login'}
            </button>
          </form>

          <div className="mt-4">
            <button
              type="button"
              onClick={() => setIsRegister(!isRegister)}
              className="text-sm text-blue-600 hover:text-blue-700"
            >
              {isRegister ? 'Already have an account? Login' : "Don't have an account? Register"}
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={handleDemoLogin}
              disabled={loading}
              className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition-colors font-medium disabled:opacity-50"
            >
              🎯 Try Demo Account
            </button>
            <p className="text-xs text-gray-500 text-center mt-2">
              Username: demo | Password: demo123
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-white text-sm">
          <p>Final Year Project - Computer Science</p>
          <p className="text-blue-100">AI-Powered DevOps Pipeline System</p>
        </div>
      </div>
    </div>
  )
}

export default Login
