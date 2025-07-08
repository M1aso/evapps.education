import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

const protectedPaths = ['/profile', '/courses', '/chat', '/notification', '/analytics']

export async function middleware(req: NextRequest) {
  const token = await getToken({ req })
  const { pathname } = req.nextUrl
  if (protectedPaths.some((path) => pathname.startsWith(path)) && !token) {
    return NextResponse.redirect(new URL('/auth', req.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ['/profile/:path*', '/courses/:path*', '/chat/:path*', '/notification/:path*', '/analytics/:path*'],
}
