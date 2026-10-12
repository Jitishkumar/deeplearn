import React, { useState, useEffect } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'

function Analytics() {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState('')
  const [analytics, setAnalytics] = useState(null)
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/api/v1/projects')
      setProjects(response.data)
      if (response.data.length > 0) {
        setSelectedProject(response.data[0].id.toString())
      }
    } catch (error) {
      toast.error('Failed to load projects')
    }
  }

  const fetchAnalytics = async () => {
    if (!selectedProject) return

    setLoading(true)
    try {
      const [analyticsRes, insightsRes] = await Promise.all([
        api.get(`/api/v1/projects/${selectedProject}/analytics`),
        api.get(`/api/v1/predict/insights/${selectedProject}`)
      ])
      setAnalytics(analyticsRes.data)
      setInsights(insightsRes.data)
    } catch (error) {
      toast.error('Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (selectedProject) {
      fetchAnalytics()
    }
  }, [selectedProject])

  const getImpactColor = (impact) => {
    return impact === 'high' ? 'text-red-600' : impact === 'medium' ? 'text-yellow-600' : 'text-green-600'
  }

  if (projects.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No projects available</h3>
        <p className="text-gray-600">Create a project and run some builds to see analytics</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics & Insights</h1>
          <p className="text-gray-600 mt-1">Comprehensive performance metrics and AI recommendations</p>
        </div>
        <select
          value={selectedProject}
          onChange={(e) => setSelectedProject(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          {projects.map(project => (
            <option key={project.id} value={project.id}>{project.name}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center p-12">
          <div className="animate-spin text-6xl">📊</div>
        </div>
      ) : analytics && insights ? (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-sm text-gray-600">Total Builds</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.summary.total_builds}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-sm text-gray-600">Success Rate</p>
              <p className="text-3xl font-bold text-green-600">{analytics.summary.success_rate.toFixed(1)}%</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-sm text-gray-600">Avg Duration</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.summary.avg_duration.toFixed(0)}s</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-sm text-gray-600">Health Score</p>
              <p className="text-3xl font-bold text-blue-600">{insights.health_score.toFixed(0)}/100</p>
            </div>
          </div>

          {/* Trends */}
          {insights.trends && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">📈 Trends</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Success Rate Trend</p>
                  <p className="text-xl font-bold capitalize">{insights.trends.success_rate_trend}</p>
                  <p className="text-sm text-gray-500">
                    {insights.trends.success_rate_change > 0 ? '+' : ''}{insights.trends.success_rate_change.toFixed(1)}%
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Duration Trend</p>
                  <p className="text-xl font-bold capitalize">{insights.trends.duration_trend}</p>
                  <p className="text-sm text-gray-500">
                    {insights.trends.duration_change_seconds > 0 ? '+' : ''}{insights.trends.duration_change_seconds.toFixed(0)}s
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Build Frequency</p>
                  <p className="text-xl font-bold">{insights.trends.build_frequency_per_day.toFixed(1)}</p>
                  <p className="text-sm text-gray-500">builds per day</p>
                </div>
              </div>
            </div>
          )}

          {/* AI Recommendations */}
          {insights.recommendations && insights.recommendations.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">🤖 AI Recommendations</h2>
              <div className="space-y-4">
                {insights.recommendations.map((rec, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-semibold text-gray-900">{rec.title}</h3>
                        <p className="text-sm text-gray-500 capitalize">{rec.category}</p>
                      </div>
                      <div className="flex space-x-2">
                        <span className={`px-2 py-1 text-xs rounded ${getImpactColor(rec.impact)} bg-opacity-10`}>
                          Impact: {rec.impact}
                        </span>
                        <span className="px-2 py-1 text-xs rounded text-blue-600 bg-blue-50">
                          Effort: {rec.effort}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{rec.description}</p>
                    <p className="text-xs text-green-600 font-medium">💡 {rec.estimated_improvement}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Anomalies */}
          {insights.anomalies && insights.anomalies.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">⚠️ Anomalies Detected</h2>
              <ul className="space-y-2">
                {insights.anomalies.map((anomaly, index) => (
                  <li key={index} className="flex items-start space-x-2 text-sm">
                    <span className="text-yellow-500">⚠️</span>
                    <span className="text-gray-700">{anomaly}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Project Recommendations */}
          {analytics.recommendations && analytics.recommendations.length > 0 && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">📋 Action Items</h2>
              <ul className="space-y-2">
                {analytics.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <span className="text-blue-600">•</span>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Busiest Hours */}
          {analytics.busiest_hours && analytics.busiest_hours.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">⏰ Busiest Hours</h2>
              <div className="flex space-x-2">
                {analytics.busiest_hours.map((hour) => (
                  <div key={hour} className="bg-blue-100 px-4 py-2 rounded-lg text-blue-900 font-medium">
                    {hour}:00
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No data available</h3>
          <p className="text-gray-600">Run some builds to generate analytics</p>
        </div>
      )}
    </div>
  )
}

export default Analytics
