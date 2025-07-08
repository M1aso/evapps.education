import CourseCard from './CourseCard'

export default function CourseList({ courses }: { courses: any[] }) {
  if (!courses?.length) return <p>No courses</p>
  return (
    <div className="grid gap-4">
      {courses.map((c) => (
        <CourseCard key={c.id} title={c.title} description={c.description} />
      ))}
    </div>
  )
}
