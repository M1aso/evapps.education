import api from './api'

export const listChats = () => api.get('/chat')
export const sendMessage = (chatId: string, message: string) =>
  api.post(`/chat/${chatId}/messages`, { message })
