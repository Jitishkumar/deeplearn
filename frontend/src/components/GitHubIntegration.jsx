import React, { useState, useEffect } from 'react'
import api from '../services/api'

const GitHubIntegration = ({ onProjectCreated }) => {
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [testRepos, setTestRepos] = useState([])
  const [selectedRepo, setSelectedRepo] = useState(null)
  const [repoInfo, setRepoInfo] = useState(null)

  useEffect(() => {
    fetchTestRepos()
  }, [])

  const fetchTestRepos = async () => {
    try {
      const response = await api.get('/api/v1/projects/github/test-repos')
      setTestRepos(response.data.repositories)
    } catch (error) {
      console.error('Failed to fetch test repos:', error)
    }
  }

  const handleCreateFromGitHub = async (url) => {
    setLoading(true)
    try {
      const response = await api.post('/api/v1/projects/github', {
        repository_url: url
      })
      
      if (onProjectCreated) {
        onProjectCreated(response.data)
      }
      
      setRepoUrl('')
      setSelectedRepo(null)
      setRepoInfo(null)
      
      // Show success message
      alert(`✅ Successfully created project: ${response.data.name}`)
      
    } catch (error) {
      console.error('Failed to create GitHub project:', error)
      alert(`❌ Failed to create project: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const TestRepoCard = ({ repo }) => (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <span className="text-xl">🔗</span>
            {repo.name}
          </h3>
          <p className="text-sm text-gray-600 mt-1">{repo.description}</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span className="text-base">💻</span>
          {repo.language}
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span>🔗</span>
          <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">
            {repo.url.replace('https://github.com/', '')}
          </span>
        </div>
        
        <button
          onClick={() => handleCreateFromGitHub(repo.url)}
          disabled={loading}
          className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-md text-sm font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span>▶️</span>
          {loading ? 'Creating...' : 'Add & Test'}
        </button>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border">
        <div className="text-6xl mb-4">🔗</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Real GitHub Integration</h2>
        <p className="text-gray-600">
          Pull actual code from GitHub repositories and run REAL tests!
        </p>
      </div>

      {/* Custom GitHub URL */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <span className="text-xl">🌿</span>
          Add Your Own GitHub Repository
        </h3>
        
        <div className="flex gap-3">
          <input
            type="url"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className="flex-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={() => handleCreateFromGitHub(repoUrl)}
            disabled={!repoUrl || loading}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <span>🔗</span>
            {loading ? 'Adding...' : 'Add Repository'}
          </button>
        </div>
        
        <p className="text-xs text-gray-500 mt-2">
          ✨ Supports Python (pytest), JavaScript (Jest/npm test), and more!
        </p>
      </div>

      {/* Test Repositories */}
      <div className="bg-white border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <span className="text-xl">⭐</span>
          Demo Repositories (Ready to Test!)
        </h3>
        
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {testRepos.map((repo, index) => (
            <TestRepoCard key={index} repo={repo} />
          ))}
        </div>
        
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">🚀 What Happens When You Add a Repository:</h4>
          <div className="space-y-2 text-sm text-blue-800">
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>Clones actual code from GitHub</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>Detects project type (Python/JavaScript/etc)</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>Installs dependencies (npm install, pip install)</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>Runs REAL tests (pytest, Jest, npm test)</span>
            </div>
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>Shows actual test results and logs!</span>
            </div>
          </div>
        </div>
      </div>

      {/* API Endpoints Info */}
      <div className="bg-gray-50 border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <span className="text-xl">💻</span>
          New API Endpoints Added
        </h3>
        
        <div className="space-y-3 text-sm font-mono">
          <div className="flex items-center gap-3">
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium">POST</span>
            <code>/api/v1/projects/github</code>
            <span className="text-gray-600">- Create project from GitHub URL</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">GET</span>
            <code>/api/v1/projects/github/test-repos</code>
            <span className="text-gray-600">- Get demo repositories</span>
          </div>
        </div>
        
        <div className="mt-4 p-3 bg-yellow-50 rounded border-l-4 border-yellow-400">
          <p className="text-sm text-yellow-800">
            <strong>🔥 This is REAL integration!</strong> Unlike the previous simulation, this actually clones repositories from GitHub and runs genuine tests on real code!
          </p>
        </div>
      </div>
    </div>
  )
}

export default GitHubIntegration