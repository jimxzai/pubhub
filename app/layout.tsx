import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '生命之道 — 約翰福音研讀',
  description: '7年三書精讀出版系統 | MVP: Gospel of John Study',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body className="font-chinese antialiased">{children}</body>
    </html>
  )
}
