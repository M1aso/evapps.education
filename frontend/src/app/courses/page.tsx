'use client'

import { useQuery } from '@tanstack/react-query'
import { listCourses } from '@/lib/content'
import CourseList from '@/components/CourseList'

export default function CoursesPage() {
  const { data } = useQuery({
    queryKey: ['courses'],
    queryFn: () => listCourses().then((res) => res.data),
  })

  return (
    <div className="p-4">
      <CourseList courses={data ?? []} />
    </div>
  )
}
