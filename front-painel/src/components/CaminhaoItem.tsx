import { FiEdit2, FiTrash2 } from 'react-icons/fi'
import type { Caminhao } from './CaminhaoForm'
import '../styles/caminhao-item.css'
import { useState } from 'react'
import { Modal } from './Modal'



interface Props {
  caminhao: Caminhao
  onEdit: () => void
  onDelete: () => void
}

export function CaminhaoItem({ caminhao, onEdit, onDelete }: Props) {
  const [confirmOpen, setConfirmOpen] = useState(false)

  return (
    <div className="caminhao-item">
      <div className="caminhao-info">
        <strong>
          {caminhao.marca} {caminhao.modelo}
        </strong>
        <span>
          {caminhao.ano} • {caminhao.tipo}
        </span>
      </div>

      <div className="caminhao-actions">
        <button title="Editar" onClick={onEdit}>
          <FiEdit2 size={16} />
        </button>
        <button
  title="Remover"
  className="danger"
  onClick={() => setConfirmOpen(true)}
>
  <FiTrash2 size={16} />
</button>

      </div>


      <Modal
  title="Confirmar exclusão"
  isOpen={confirmOpen}
  onClose={() => setConfirmOpen(false)}
>
  <p style={{ fontSize: '14px', color: 'var(--text-muted)' }}>
    Deseja realmente excluir este caminhão?
  </p>

  <div
    style={{
      display: 'flex',
      justifyContent: 'flex-end',
      gap: '10px',
      marginTop: '20px',
    }}
  >
    <button
      onClick={() => setConfirmOpen(false)}
      style={{
        background: 'transparent',
        color: 'var(--text-muted)',
        padding: '6px 12px',
        borderRadius: '6px',
      }}
    >
      Cancelar
    </button>
    <button
  onClick={() => {
    onDelete()
    setConfirmOpen(false)
  }}
  style={{
    background: '#ff5f5f',
    color: '#fff',
    padding: '6px 14px',
    borderRadius: '6px',
  }}
>
  Remover
</button>

  </div>
</Modal>

    </div>

    
  )
}
