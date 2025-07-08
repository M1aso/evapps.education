'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import Button from '@/components/Button'
import Input from '@/components/Input'

export default function LoginPage() {
  const [tab, setTab] = useState<'phone' | 'email'>('phone')
  const [phone, setPhone] = useState('')
  const [code, setCode] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleEmail = async () => {
    await signIn('credentials', { email, password, redirect: false })
  }

  const handlePhone = async () => {
    await signIn('credentials', { phone, password: code, redirect: false })
  }

  return (
    <div className="max-w-sm mx-auto p-4 space-y-4">
      <div className="flex space-x-2">
        <button
          onClick={() => setTab('phone')}
          className={tab === 'phone' ? 'font-bold' : ''}
        >
          Phone
        </button>
        <button
          onClick={() => setTab('email')}
          className={tab === 'email' ? 'font-bold' : ''}
        >
          Email
        </button>
      </div>

      {tab === 'phone' ? (
        <div className="space-y-2">
          <Input
            placeholder="+7..."
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
          <Input
            placeholder="Code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <Button onClick={handlePhone}>Login</Button>
        </div>
      ) : (
        <div className="space-y-2">
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button onClick={handleEmail}>Login</Button>
        </div>
      )}
    </div>
  )
}
