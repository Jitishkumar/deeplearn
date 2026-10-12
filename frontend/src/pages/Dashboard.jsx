import React, { useState, useEffect } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [dashboard, setDashboard] = useState(null)

  useEffect(() => {
    fetchDashboard()
    const interval = setInterval(fetchDashboard, 10000) // Refresh every 10s
    return () => clearInterval(interval)
  }, [])

  const fetchDashboard = async () => {
    try {
      const response = await api.get('/api/v1/dashboard')
      setDashboard(response.data)
      setLoading(false)
    } catch (error) {
      toast.error('Failed to load dashboard')
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin text-6xl mb-4">⚙️</div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  const getStatusColor = (status) => {
    const colors = {
      success: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      running: 'bg-blue-100 text-blue-800',
      pending: 'bg-yellow-100 text-yellow-800',
      cancelled: 'bg-gray-100 text-gray-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getHealthColor = (health) => {
    const colors = {
      healthy: 'text-green-600',
      degraded: 'text-yellow-600',
      down: 'text-red-600',
    }
    return colors[health] || 'text-gray-600'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Monitor your CI/CD pipeline performance in real-time</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Projects</p>
              <p className="text-3xl font-bold text-gray-900">{dashboard.total_projects}</p>
            </div>
            <div className="text-4xl">📁</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Builds Today</p>
              <p className="text-3xl font-bold text-gray-900">{dashboard.total_builds_today}</p>
            </div>
            <div className="text-4xl">🔨</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Builds</p>
              <p className="text-3xl font-bold text-blue-600">{dashboard.active_builds}</p>
            </div>
            <div className="text-4xl animate-pulse">⚙️</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Success Rate</p>
              <p className="text-3xl font-bold text-green-600">{dashboard.success_rate_today.toFixed(1)}%</p>
            </div>
            <div className="text-4xl">✅</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg Build Time</p>
              <p className="text-3xl font-bold text-gray-900">{dashboard.avg_build_time.toFixed(0)}s</p>
            </div>
            <div className="text-4xl">⏱️</div>
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">System Health</h2>
        <div className="flex items-center space-x-4">
          <div className={`text-4xl ${getHealthColor(dashboard.system_health)}`}>
            {dashboard.system_health === 'healthy' ? '💚' : dashboard.system_health === 'degraded' ? '💛' : '❤️'}
          </div>
          <div>
            <p className="text-2xl font-bold capitalize">{dashboard.system_health}</p>
            <p className="text-gray-600">
              {dashboard.system_health === 'healthy' && 'All systems operational'}
              {dashboard.system_health === 'degraded' && 'Some issues detected'}
              {dashboard.system_health === 'down' && 'Critical issues present'}
            </p>
          </div>
        </div>
      </div>

      {/* Recent Builds */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Recent Builds</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Build ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Project
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Branch
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duration
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {dashboard.recent_builds.map((build) => (
                <tr key={build.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{build.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    Project {build.project_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <code className="bg-gray-100 px-2 py-1 rounded">{build.branch}</code>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(build.status)}`}>
                      {build.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {build.duration ? `${build.duration}s` : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(build.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-6 rounded-lg shadow-md text-white cursor-pointer hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">🚀</div>
          <h3 className="text-xl font-semibold mb-2">Trigger Build</h3>
          <p className="text-blue-100">Start a new pipeline build</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 p-6 rounded-lg shadow-md text-white cursor-pointer hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">🤖</div>
          <h3 className="text-xl font-semibold mb-2">AI Predictions</h3>
          <p className="text-purple-100">Get build failure predictions</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 p-6 rounded-lg shadow-md text-white cursor-pointer hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">📊</div>
          <h3 className="text-xl font-semibold mb-2">View Analytics</h3>
          <p className="text-green-100">Explore performance metrics</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
