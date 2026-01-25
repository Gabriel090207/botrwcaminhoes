import { useState } from 'react'
import { Sidebar } from './Sidebar'
import { Header } from './Header'
import '../styles/painel.css'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="layout">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="main">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        <div className="content">{children}</div>
      </div>
    </div>
  )
}
