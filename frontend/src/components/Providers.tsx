// app/Providers.tsx
'use client'

import { ReactNode } from 'react'
import { SessionProvider } from 'next-auth/react'
import QueryClientProviderWrapper from '../components/QueryClientProviderWrapper'

type Props = { children: ReactNode }

export default function Providers({ children }: Props) {
  return (
    <SessionProvider>
      <QueryClientProviderWrapper>
        {children}
      </QueryClientProviderWrapper>
    </SessionProvider>
  )
}

