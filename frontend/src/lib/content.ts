import api from './api'

// Content service routes are served under the `/content` prefix via the
// Nginx gateway. The service itself exposes endpoints under `/api`, so the
// final paths become `/content/api/...` when accessed through the gateway.
export const listCourses = () => api.get('/content/api/courses')
export const getCourse = (id: string) => api.get(`/content/api/courses/${id}`)
