import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

const protectedPaths = ['/profile', '/courses', '/chat', '/notification', '/analytics']

export async function middleware(req: NextRequest) {
  const token = await getToken({ req })
  const { pathname } = req.nextUrl
  const [, locale, ...rest] = pathname.split('/')
  const path = '/' + rest.join('/')
  if (protectedPaths.some((p) => path.startsWith(p)) && !token) {
    return NextResponse.redirect(new URL(`/${locale}/auth`, req.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/:locale/profile/:path*',
    '/:locale/courses/:path*',
    '/:locale/chat/:path*',
    '/:locale/notification/:path*',
    '/:locale/analytics/:path*',
  ],
}
