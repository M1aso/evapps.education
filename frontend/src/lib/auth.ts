import api from './api'

export const login = (data: { email?: string; phone?: string; password: string }) =>
  api.post('/auth/login', data)

export const register = (data: { email?: string; phone?: string; password: string }) =>
  api.post('/auth/register', data)
