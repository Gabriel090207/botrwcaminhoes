import { useEffect, useState } from 'react'
import '../styles/modal.css'

interface ModalProps {
  title: string
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}

export function Modal({ title, isOpen, onClose, children }: ModalProps) {
  const [visible, setVisible] = useState(isOpen)
  const [animation, setAnimation] = useState<'modal-enter' | 'modal-exit'>(
    'modal-enter'
  )

  useEffect(() => {
    if (isOpen) {
      setVisible(true)
      setAnimation('modal-enter')
    } else {
      setAnimation('modal-exit')

      const timeout = setTimeout(() => {
        setVisible(false)
      }, 250) // tempo igual à animação de saída

      return () => clearTimeout(timeout)
    }
  }, [isOpen])

  if (!visible) return null

  return (
    <div className="modal-overlay">
      <div className={`modal-box ${animation}`}>
        <header className="modal-header">
          <h3>{title}</h3>
          <button onClick={onClose}>✕</button>
        </header>

        <div className="modal-content">{children}</div>
      </div>
    </div>
  )
}
