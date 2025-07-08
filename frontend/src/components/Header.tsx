'use client'

import Link from 'next/link'
import { useSession, signOut } from 'next-auth/react'

export default function Header() {
  const { data: session } = useSession()

  return (
    <header className="flex items-center justify-between p-4 border-b">
      <Link href="/courses" className="font-bold">
        Logo
      </Link>
      <nav className="space-x-4">
        <Link href="/courses">Courses</Link>
        <Link href="/chat">Chat</Link>
        <Link href="/notification">Notifications</Link>
        <Link href="/analytics">Analytics</Link>
        {session && <Link href="/profile">Profile</Link>}
      </nav>
      {session ? (
        <button onClick={() => signOut()} className="text-sm">
          Logout
        </button>
      ) : (
        <Link href="/auth/login">Login</Link>
      )}
    </header>
  )
}
