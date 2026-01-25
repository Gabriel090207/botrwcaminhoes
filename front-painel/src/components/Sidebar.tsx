import { Link, useLocation } from 'react-router-dom'
import { FiGrid, FiTruck, FiSettings, FiX } from 'react-icons/fi'
import { useEffect } from 'react'

import '../styles/sidebar.css'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation()

  useEffect(() => {
    if (isOpen) {
      document.body.classList.add('sidebar-open')
    } else {
      document.body.classList.remove('sidebar-open')
    }
  
    return () => {
      document.body.classList.remove('sidebar-open')
    }
  }, [isOpen])
  

  return (
    <>
      {/* Overlay (mobile) */}
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}

      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            RW Caminhões
            <span>Painel</span>
          </div>

          {/* Botão fechar (mobile) */}
          <button className="sidebar-close" onClick={onClose}>
            <FiX size={22} />
          </button>
        </div>

        <nav className="sidebar-menu">
          <Link
            to="/"
            onClick={onClose}
            className={location.pathname === '/' ? 'active' : ''}
          >
            <FiGrid size={16} />
            Dashboard
          </Link>

          <Link
            to="/caminhoes"
            onClick={onClose}
            className={location.pathname === '/caminhoes' ? 'active' : ''}
          >
            <FiTruck size={16} />
            Caminhões
          </Link>

          <Link
            to="/ajustes"
            onClick={onClose}
            className={location.pathname === '/ajustes' ? 'active' : ''}
          >
            <FiSettings size={16} />
            Ajustes do Bot
          </Link>
        </nav>
      </aside>
    </>
  )
}
