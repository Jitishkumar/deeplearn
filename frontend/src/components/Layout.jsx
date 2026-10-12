import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

function Layout({ children, onLogout }) {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const menuItems = [
    { path: '/', icon: '📊', label: 'Dashboard' },
    { path: '/projects', icon: '📁', label: 'Projects' },
    { path: '/pipelines', icon: '🔄', label: 'Pipelines' },
    { path: '/predictions', icon: '🤖', label: 'AI Predictions' },
    { path: '/analytics', icon: '📈', label: 'Analytics' },
  ]

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-gray-900 text-white transition-all duration-300 flex flex-col`}>
        {/* Logo */}
        <div className="p-4 border-b border-gray-800">
          <div className="flex items-center justify-between">
            {sidebarOpen ? (
              <h1 className="text-xl font-bold">🚀 AI DevOps</h1>
            ) : (
              <span className="text-2xl">🚀</span>
            )}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-400 hover:text-white"
            >
              {sidebarOpen ? '◀' : '▶'}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                {sidebarOpen && <span className="font-medium">{item.label}</span>}
              </Link>
            )
          })}
        </nav>

        {/* User section */}
        <div className="p-4 border-t border-gray-800">
          {sidebarOpen ? (
            <button
              onClick={onLogout}
              className="w-full flex items-center space-x-3 px-4 py-3 text-gray-300 hover:bg-gray-800 hover:text-white rounded-lg transition-colors"
            >
              <span className="text-xl">🚪</span>
              <span>Logout</span>
            </button>
          ) : (
            <button
              onClick={onLogout}
              className="w-full text-xl hover:text-red-400 transition-colors"
              title="Logout"
            >
              🚪
            </button>
          )}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}

export default Layout
