import React, { useState, useEffect } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'

function Projects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    repository_url: '',
    language: 'python',
    branch: 'main'
  })

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/api/v1/projects')
      setProjects(response.data)
      setLoading(false)
    } catch (error) {
      toast.error('Failed to load projects')
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/v1/projects', formData)
      toast.success('Project created successfully!')
      setShowModal(false)
      setFormData({ name: '', description: '', repository_url: '', language: 'python', branch: 'main' })
      fetchProjects()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create project')
    }
  }

  const handleDelete = async (projectId) => {
    if (!window.confirm('Are you sure you want to delete this project?')) return
    
    try {
      await api.delete(`/api/v1/projects/${projectId}`)
      toast.success('Project deleted')
      fetchProjects()
    } catch (error) {
      toast.error('Failed to delete project')
    }
  }

  if (loading) {
    return <div className="flex justify-center p-8"><div className="animate-spin text-4xl">⚙️</div></div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-600 mt-1">Manage your development projects</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          ➕ New Project
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <div className="text-6xl mb-4">📁</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No projects yet</h3>
          <p className="text-gray-600 mb-4">Create your first project to get started</p>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Create Project
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div key={project.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">{project.name}</h3>
                  <p className="text-sm text-gray-500">{project.language.toUpperCase()}</p>
                </div>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full">
                  {project.branch}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{project.description || 'No description'}</p>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500">Total Builds</p>
                  <p className="text-2xl font-bold text-gray-900">{project.total_builds}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Success Rate</p>
                  <p className="text-2xl font-bold text-green-600">{project.success_rate.toFixed(1)}%</p>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                  View Details
                </button>
                <button
                  onClick={() => handleDelete(project.id)}
                  className="bg-red-100 text-red-600 px-4 py-2 rounded-lg hover:bg-red-200 transition-colors text-sm"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Project Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">Create New Project</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Project Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="my-awesome-project"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Project description..."
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Repository URL</label>
                <input
                  type="url"
                  value={formData.repository_url}
                  onChange={(e) => setFormData({...formData, repository_url: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="https://github.com/user/repo"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Language *</label>
                <select
                  value={formData.language}
                  onChange={(e) => setFormData({...formData, language: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="python">Python</option>
                  <option value="nodejs">Node.js</option>
                  <option value="java">Java</option>
                  <option value="go">Go</option>
                  <option value="ruby">Ruby</option>
                  <option value="php">PHP</option>
                  <option value="other">Other</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Default Branch</label>
                <input
                  type="text"
                  value={formData.branch}
                  onChange={(e) => setFormData({...formData, branch: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="main"
                />
              </div>
              
              <div className="flex space-x-3">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Create Project
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Projects
