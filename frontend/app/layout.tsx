import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EY Agentic AI - Automotive Aftersales Predictive Maintenance',
  description: 'Real-time predictive maintenance ecosystem for automotive aftersales',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

