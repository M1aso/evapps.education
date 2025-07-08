import api from './api'

export const getProfile = () => api.get('/profile/me')
export const updateProfile = (data: any) => api.put('/profile/me', data)
