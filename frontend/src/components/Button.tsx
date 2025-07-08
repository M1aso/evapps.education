interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
}

export default function Button({ children, ...props }: Props) {
  return (
    <button
      {...props}
      className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
    >
      {children}
    </button>
  )
}
