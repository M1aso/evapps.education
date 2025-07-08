import api from './api'

export const listNotifications = () => api.get('/notification')
export const markRead = (id: string) => api.post(`/notification/${id}/read`)
