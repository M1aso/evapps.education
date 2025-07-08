import api from './api'

export const listCourses = () => api.get('/courses')
export const getCourse = (id: string) => api.get(`/courses/${id}`)
