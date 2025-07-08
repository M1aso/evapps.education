import CourseCard from './CourseCard'

interface Course {
  id: string
  title: string
  description: string
}

export default function CourseList({ courses }: { courses?: Course[] }) {
  // API responses may not always be the expected array (e.g. error objects).
  // Guard against those cases to avoid runtime errors.
  console.log(courses);
  if (!Array.isArray(courses) || courses.length === 0) return <p>No courses</p>
  return (
    <div className="grid gap-4">
      {courses.map((c) => (
        <CourseCard key={c.id} title={c.title} description={c.description} />
      ))}
    </div>
  )
}
