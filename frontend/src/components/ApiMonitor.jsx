import React, { useState, useEffect, useRef } from 'react'
import api from '../services/api'

const ApiMonitor = () => {
  const [requests, setRequests] = useState([])
  const [stats, setStats] = useState({
    total: 0,
    success: 0,
    failed: 0,
    avgResponseTime: 0
  })
  const requestLogRef = useRef([])

  useEffect(() => {
    // Intercept Axios requests (not window.fetch - axios uses XMLHttpRequest)
    const requestInterceptor = api.interceptors.request.use(
      (config) => {
        config._startTime = Date.now()
        return config
      },
      (error) => Promise.reject(error)
    )

    const responseInterceptor = api.interceptors.response.use(
      (response) => {
        const duration = Date.now() - (response.config._startTime || Date.now())
        const logEntry = {
          id: Date.now() + Math.random(),
          method: (response.config.method || 'GET').toUpperCase(),
          url: response.config.url || '',
          status: response.status,
          duration,
          timestamp: new Date().toISOString(),
          success: response.status >= 200 && response.status < 300
        }

        requestLogRef.current = [logEntry, ...requestLogRef.current].slice(0, 50)
        setRequests([...requestLogRef.current])
        updateStats(requestLogRef.current)

        return response
      },
      (error) => {
        const duration = Date.now() - (error.config?._startTime || Date.now())
        const logEntry = {
          id: Date.now() + Math.random(),
          method: (error.config?.method || 'GET').toUpperCase(),
          url: error.config?.url || 'unknown',
          status: error.response?.status || 0,
          duration,
          timestamp: new Date().toISOString(),
          success: false,
          error: error.message
        }

        requestLogRef.current = [logEntry, ...requestLogRef.current].slice(0, 50)
        setRequests([...requestLogRef.current])
        updateStats(requestLogRef.current)

        return Promise.reject(error)
      }
    )

    // Do an initial health check to populate the monitor
    api.get('/health').catch(() => {})
    api.get('/api/v1/dashboard').catch(() => {})

    return () => {
      api.interceptors.request.eject(requestInterceptor)
      api.interceptors.response.eject(responseInterceptor)
    }
  }, [])

  const updateStats = (requestLog) => {
    const total = requestLog.length
    const success = requestLog.filter(r => r.success).length
    const failed = total - success
    const avgResponseTime = total > 0 
      ? Math.round(requestLog.reduce((sum, r) => sum + r.duration, 0) / total)
      : 0

    setStats({ total, success, failed, avgResponseTime })
  }

  const getStatusColor = (status) => {
    if (status >= 200 && status < 300) return 'text-green-600 bg-green-100'
    if (status >= 400 && status < 500) return 'text-yellow-600 bg-yellow-100'
    if (status >= 500) return 'text-red-600 bg-red-100'
    return 'text-gray-600 bg-gray-100'
  }

  const getMethodColor = (method) => {
    const colors = {
      GET: 'bg-blue-100 text-blue-700',
      POST: 'bg-green-100 text-green-700',
      PUT: 'bg-yellow-100 text-yellow-700',
      DELETE: 'bg-red-100 text-red-700',
      PATCH: 'bg-purple-100 text-purple-700'
    }
    return colors[method] || 'bg-gray-100 text-gray-700'
  }

  const formatDuration = (ms) => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(2)}s`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <span className="text-3xl">📡</span>
            Live API Monitor
          </h2>
          <p className="text-gray-600 mt-1">Real-time HTTP request tracking (Axios interceptors)</p>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-gray-600">Live</span>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium">Total Requests</p>
              <p className="text-3xl font-bold text-blue-900 mt-1">{stats.total}</p>
            </div>
            <span className="text-3xl opacity-50">🖥️</span>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 font-medium">Successful</p>
              <p className="text-3xl font-bold text-green-900 mt-1">{stats.success}</p>
              <p className="text-xs text-green-700 mt-1">
                {stats.total > 0 ? `${((stats.success / stats.total) * 100).toFixed(1)}%` : '0%'}
              </p>
            </div>
            <span className="text-3xl opacity-50">✅</span>
          </div>
        </div>

        <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-6 border border-red-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600 font-medium">Failed</p>
              <p className="text-3xl font-bold text-red-900 mt-1">{stats.failed}</p>
              <p className="text-xs text-red-700 mt-1">
                {stats.total > 0 ? `${((stats.failed / stats.total) * 100).toFixed(1)}%` : '0%'}
              </p>
            </div>
            <span className="text-3xl opacity-50">❌</span>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6 border border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-600 font-medium">Avg Response</p>
              <p className="text-3xl font-bold text-purple-900 mt-1">{stats.avgResponseTime}ms</p>
              <p className="text-xs text-purple-700 mt-1">
                {stats.avgResponseTime < 100 ? '⚡ Fast' : stats.avgResponseTime < 500 ? '✅ Good' : '⚠️ Slow'}
              </p>
            </div>
            <span className="text-3xl opacity-50">⚡</span>
          </div>
        </div>
      </div>

      {/* Request Table */}
      <div className="bg-white rounded-lg shadow-md border overflow-hidden">
        <div className="px-6 py-4 bg-gray-50 border-b flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            📊 Recent API Requests
          </h3>
          <span className="text-xs text-gray-500">Navigate the app to see requests appear here</span>
        </div>
        
        <div className="overflow-x-auto">
          {requests.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <div className="text-5xl mb-4 opacity-50">📡</div>
              <p className="text-lg font-medium">No requests captured yet</p>
              <p className="text-sm mt-2">Navigate to other pages (Dashboard, Projects, Pipelines) to see API requests here</p>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Endpoint</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {requests.slice(0, 30).map((request) => (
                  <tr key={request.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-3 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${getMethodColor(request.method)}`}>
                        {request.method}
                      </span>
                    </td>
                    <td className="px-6 py-3">
                      <span className="text-sm text-gray-900 font-mono">{request.url}</span>
                    </td>
                    <td className="px-6 py-3 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(request.status)}`}>
                        {request.status || 'ERR'}
                      </span>
                    </td>
                    <td className="px-6 py-3 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="text-sm">⏱️</span>
                        <span className={`text-sm font-medium ${
                          request.duration < 100 ? 'text-green-600' : 
                          request.duration < 500 ? 'text-yellow-600' : 
                          'text-red-600'
                        }`}>
                          {formatDuration(request.duration)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-3 whitespace-nowrap text-sm text-gray-500">
                      {new Date(request.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* API Endpoints Reference */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6 border border-indigo-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">📡 Available API Endpoints</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">GET</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/projects</code>
          </div>
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-green-600 bg-green-100 px-2 py-1 rounded">POST</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/projects/github</code>
          </div>
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">GET</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/pipelines</code>
          </div>
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-green-600 bg-green-100 px-2 py-1 rounded">POST</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/pipelines/trigger</code>
          </div>
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-green-600 bg-green-100 px-2 py-1 rounded">POST</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/predict/failure</code>
          </div>
          <div className="bg-white rounded p-3 border border-indigo-100">
            <span className="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">GET</span>
            <code className="text-sm text-gray-700 ml-2">/api/v1/dashboard</code>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ApiMonitor