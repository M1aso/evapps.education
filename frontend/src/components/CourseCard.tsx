interface Props {
  title: string
  description: string
}

export default function CourseCard({ title, description }: Props) {
  return (
    <div className="border rounded p-4">
      <h3 className="font-bold">{title}</h3>
      <p>{description}</p>
    </div>
  )
}
