export default function Footer() {
  return (
    <footer className="p-4 border-t text-center text-sm mt-auto">
      © {new Date().getFullYear()} <a href="/privacy">Privacy Policy</a>
    </footer>
  )
}
