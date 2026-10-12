import api from './api'

export const login = async (username, password) => {
  // Send as JSON instead of form data
  const response = await api.post('/api/v1/auth/login', {
    username,
    password,
  })
  
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token)
  }
  
  return response.data
}

export const register = async (email, username, password, fullName) => {
  const response = await api.post('/api/v1/auth/register', {
    email,
    username,
    password,
    full_name: fullName,
  })
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/api/v1/auth/me')
  return response.data
}

export const logout = () => {
  localStorage.removeItem('token')
}

export const getToken = () => {
  return localStorage.getItem('token')
}

export const isAuthenticated = () => {
  return !!getToken()
}
