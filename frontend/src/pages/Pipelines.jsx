import React, { useState, useEffect } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'

function Pipelines() {
  const [pipelines, setPipelines] = useState([])
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [selectedProject, setSelectedProject] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [pipelinesRes, projectsRes] = await Promise.all([
        api.get('/api/v1/pipelines'),
        api.get('/api/v1/projects')
      ])
      setPipelines(pipelinesRes.data)
      setProjects(projectsRes.data)
      setLoading(false)
    } catch (error) {
      toast.error('Failed to load data')
      setLoading(false)
    }
  }

  const triggerBuild = async () => {
    if (!selectedProject) {
      toast.error('Please select a project')
      return
    }

    try {
      await api.post('/api/v1/pipelines/trigger', {
        project_id: parseInt(selectedProject),
        branch: 'main',
        triggered_by: 'manual'
      })
      toast.success('Build triggered successfully!')
      setShowModal(false)
      setSelectedProject('')
      setTimeout(fetchData, 1000)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to trigger build')
    }
  }

  const getStatusBadge = (status) => {
    const badges = {
      success: { bg: 'bg-green-100', text: 'text-green-800', icon: '✅' },
      failed: { bg: 'bg-red-100', text: 'text-red-800', icon: '❌' },
      running: { bg: 'bg-blue-100', text: 'text-blue-800', icon: '⚙️' },
      pending: { bg: 'bg-yellow-100', text: 'text-yellow-800', icon: '⏳' },
      cancelled: { bg: 'bg-gray-100', text: 'text-gray-800', icon: '🚫' },
    }
    const badge = badges[status] || badges.pending
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${badge.bg} ${badge.text} inline-flex items-center space-x-1`}>
        <span>{badge.icon}</span>
        <span>{status.toUpperCase()}</span>
      </span>
    )
  }

  if (loading) {
    return <div className="flex justify-center p-8"><div className="animate-spin text-4xl">⚙️</div></div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Pipeline Builds</h1>
          <p className="text-gray-600 mt-1">Monitor and manage your build executions</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          🚀 Trigger Build
        </button>
      </div>

      {pipelines.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <div className="text-6xl mb-4">🔄</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No builds yet</h3>
          <p className="text-gray-600 mb-4">Trigger your first build to see it here</p>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Trigger Build
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Build #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Project</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Branch</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">AI Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Started</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {pipelines.map((pipeline) => (
                <tr key={pipeline.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm font-medium text-gray-900">#{pipeline.id}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {projects.find(p => p.id === pipeline.project_id)?.name || `Project ${pipeline.project_id}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <code className="bg-gray-100 px-2 py-1 rounded text-xs">{pipeline.branch}</code>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(pipeline.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {pipeline.duration ? `${pipeline.duration}s` : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {pipeline.prediction_score ? (
                      <span className={`font-medium ${pipeline.prediction_score > 0.7 ? 'text-red-600' : pipeline.prediction_score > 0.4 ? 'text-yellow-600' : 'text-green-600'}`}>
                        {(pipeline.prediction_score * 100).toFixed(0)}%
                      </span>
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {pipeline.started_at ? new Date(pipeline.started_at).toLocaleString() : 'Not started'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button className="text-blue-600 hover:text-blue-800 mr-3">View Logs</button>
                    {(pipeline.status === 'pending' || pipeline.status === 'running') && (
                      <button className="text-red-600 hover:text-red-800">Cancel</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Trigger Build Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">Trigger New Build</h2>
            
            {projects.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No projects available. Create a project first.</p>
                <button
                  onClick={() => setShowModal(false)}
                  className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
                >
                  Close
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Select Project *
                  </label>
                  <select
                    value={selectedProject}
                    onChange={(e) => setSelectedProject(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Choose a project...</option>
                    {projects.map((project) => (
                      <option key={project.id} value={project.id}>
                        {project.name} ({project.language.toUpperCase()})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    ℹ️ The build will run on the <code className="bg-blue-100 px-2 py-1 rounded">main</code> branch with default configuration.
                  </p>
                </div>

                <div className="flex space-x-3">
                  <button
                    onClick={triggerBuild}
                    disabled={!selectedProject}
                    className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    🚀 Trigger Build
                  </button>
                  <button
                    onClick={() => {
                      setShowModal(false)
                      setSelectedProject('')
                    }}
                    className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Pipelines
