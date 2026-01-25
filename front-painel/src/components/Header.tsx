import { FiMoon, FiSun, FiMenu } from 'react-icons/fi'


import '../styles/header.css'

import { useEffect, useState } from 'react'


interface HeaderProps {
    onMenuClick: () => void
  }
  
  export function Header({ onMenuClick }: HeaderProps) {


    const [theme, setTheme] = useState<'dark' | 'light'>('dark')

useEffect(() => {
  const savedTheme = localStorage.getItem('theme') as 'dark' | 'light'

  if (savedTheme) {
    setTheme(savedTheme)
    document.documentElement.setAttribute('data-theme', savedTheme)
  }
}, [])

function toggleTheme() {
  const newTheme = theme === 'dark' ? 'light' : 'dark'
  setTheme(newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
  localStorage.setItem('theme', newTheme)
}

  
  return (
    <header className="header">
    <button className="menu-button" onClick={onMenuClick}>
      <FiMenu size={22} />
    </button>
  
    <div className="header-left">
      <h2>Dashboard</h2>
    </div>
  

      <div className="header-right">
      <button className="theme-btn" onClick={toggleTheme}>
  {theme === 'dark' ? (
    <>
      <FiMoon size={16} />
      <span>Tema escuro</span>
    </>
  ) : (
    <>
      <FiSun size={16} />
      <span>Tema claro</span>
    </>
  )}
</button>


        <div className="user-info">
          <div className="avatar">AM</div>

          <div className="user-text">
            <strong>Administrador Master</strong>
            <span>Administrador</span>
          </div>
        </div>
      </div>
    </header>
  )
}
