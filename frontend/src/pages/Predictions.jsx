import React, { useState, useEffect } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'

function Predictions() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)
  const [failureForm, setFailureForm] = useState({
    project_id: '',
    files_changed: 10,
    lines_changed: 200
  })
  const [durationForm, setDurationForm] = useState({
    project_id: '',
    language: 'python',
    files_changed: 10,
    lines_changed: 200
  })
  const [failurePrediction, setFailurePrediction] = useState(null)
  const [durationPrediction, setDurationPrediction] = useState(null)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/api/v1/projects')
      setProjects(response.data)
    } catch (error) {
      toast.error('Failed to load projects')
    }
  }

  const predictFailure = async (e) => {
    e.preventDefault()
    if (!failureForm.project_id) {
      toast.error('Please select a project')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/api/v1/predict/failure', {
        project_id: parseInt(failureForm.project_id),
        branch: 'main',
        files_changed: parseInt(failureForm.files_changed),
        lines_changed: parseInt(failureForm.lines_changed)
      })
      setFailurePrediction(response.data)
      toast.success('Prediction generated!')
    } catch (error) {
      toast.error('Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const predictDuration = async (e) => {
    e.preventDefault()
    if (!durationForm.project_id) {
      toast.error('Please select a project')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/api/v1/predict/duration', {
        project_id: parseInt(durationForm.project_id),
        language: durationForm.language,
        files_changed: parseInt(durationForm.files_changed),
        lines_changed: parseInt(durationForm.lines_changed)
      })
      setDurationPrediction(response.data)
      toast.success('Duration estimated!')
    } catch (error) {
      toast.error('Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Predictions</h1>
        <p className="text-gray-600 mt-1">Use machine learning to predict build outcomes</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Failure Prediction */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center">
            <span className="mr-2">🤖</span>
            Build Failure Prediction
          </h2>
          
          <form onSubmit={predictFailure} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Project</label>
              <select
                value={failureForm.project_id}
                onChange={(e) => setFailureForm({...failureForm, project_id: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select a project...</option>
                {projects.map(project => (
                  <option key={project.id} value={project.id}>{project.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Files Changed: {failureForm.files_changed}
              </label>
              <input
                type="range"
                min="1"
                max="50"
                value={failureForm.files_changed}
                onChange={(e) => setFailureForm({...failureForm, files_changed: e.target.value})}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lines Changed: {failureForm.lines_changed}
              </label>
              <input
                type="range"
                min="10"
                max="2000"
                step="10"
                value={failureForm.lines_changed}
                onChange={(e) => setFailureForm({...failureForm, lines_changed: e.target.value})}
                className="w-full"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Predicting...' : 'Predict Failure Risk'}
            </button>
          </form>

          {failurePrediction && (
            <div className="mt-6 space-y-4">
              <div className={`p-4 rounded-lg ${failurePrediction.risk_level === 'high' ? 'bg-red-100' : failurePrediction.risk_level === 'medium' ? 'bg-yellow-100' : 'bg-green-100'}`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">Risk Level</span>
                  <span className="text-2xl font-bold uppercase">{failurePrediction.risk_level}</span>
                </div>
                <div className="text-sm text-gray-700">
                  Failure Probability: <strong>{(failurePrediction.failure_probability * 100).toFixed(1)}%</strong>
                </div>
                <div className="text-sm text-gray-700">
                  Confidence: <strong>{(failurePrediction.confidence * 100).toFixed(0)}%</strong>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-700"><strong>Recommendation:</strong></p>
                <p className="text-sm text-gray-600 mt-1">{failurePrediction.recommendation}</p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-semibold text-gray-700 mb-2">Risk Factors:</p>
                <div className="space-y-1">
                  {Object.entries(failurePrediction.factors).map(([key, value]) => (
                    <div key={key} className="flex items-center text-sm">
                      <span className={value ? 'text-red-600' : 'text-green-600'}>
                        {value ? '⚠️' : '✅'}
                      </span>
                      <span className="ml-2 text-gray-600">{key.replace(/_/g, ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Duration Prediction */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center">
            <span className="mr-2">⏱️</span>
            Build Duration Prediction
          </h2>
          
          <form onSubmit={predictDuration} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Project</label>
              <select
                value={durationForm.project_id}
                onChange={(e) => setDurationForm({...durationForm, project_id: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select a project...</option>
                {projects.map(project => (
                  <option key={project.id} value={project.id}>{project.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
              <select
                value={durationForm.language}
                onChange={(e) => setDurationForm({...durationForm, language: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="python">Python</option>
                <option value="nodejs">Node.js</option>
                <option value="java">Java</option>
                <option value="go">Go</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Files Changed: {durationForm.files_changed}
              </label>
              <input
                type="range"
                min="1"
                max="50"
                value={durationForm.files_changed}
                onChange={(e) => setDurationForm({...durationForm, files_changed: e.target.value})}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lines Changed: {durationForm.lines_changed}
              </label>
              <input
                type="range"
                min="10"
                max="2000"
                step="10"
                value={durationForm.lines_changed}
                onChange={(e) => setDurationForm({...durationForm, lines_changed: e.target.value})}
                className="w-full"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Estimating...' : 'Estimate Duration'}
            </button>
          </form>

          {durationPrediction && (
            <div className="mt-6 space-y-4">
              <div className="bg-purple-100 p-4 rounded-lg">
                <div className="text-center">
                  <p className="text-sm text-gray-700 mb-2">Estimated Build Time</p>
                  <p className="text-4xl font-bold text-purple-900">
                    {Math.floor(durationPrediction.estimated_duration / 60)}m {durationPrediction.estimated_duration % 60}s
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    Range: {Math.floor(durationPrediction.range_min / 60)}m {durationPrediction.range_min % 60}s - {Math.floor(durationPrediction.range_max / 60)}m {durationPrediction.range_max % 60}s
                  </p>
                  <p className="text-sm text-gray-600">
                    Confidence: {(durationPrediction.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-semibold text-gray-700 mb-2">Duration Factors:</p>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Files Impact:</span>
                    <span className="font-medium">{durationPrediction.factors.files_impact}s</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Lines Impact:</span>
                    <span className="font-medium">{durationPrediction.factors.lines_impact}s</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Test Impact:</span>
                    <span className="font-medium">{durationPrediction.factors.test_impact}s</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Language Factor:</span>
                    <span className="font-medium">{durationPrediction.factors.language_factor}x</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 How it works</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Our ML models analyze historical build data to make predictions</li>
          <li>• Failure predictions help you catch issues before they happen</li>
          <li>• Duration estimates help with resource planning and scheduling</li>
          <li>• Prediction accuracy improves as more builds are completed</li>
        </ul>
      </div>
    </div>
  )
}

export default Predictions
