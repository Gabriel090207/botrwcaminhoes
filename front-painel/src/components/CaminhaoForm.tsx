import { useState, useRef } from 'react'
import '../styles/caminhao-form.css'

export interface Caminhao {
  id: string
  marca: string
  modelo: string
  ano: string
  tipo: string
  quantidade: string

  resumo: string
  observacao: string
}

interface CaminhaoFormProps {
  initialData?: Caminhao
  onSave: (data: Caminhao) => void
}

export function CaminhaoForm({ initialData, onSave }: CaminhaoFormProps) {
  const [form, setForm] = useState<Caminhao>(
    initialData || {
      id: crypto.randomUUID(),
      marca: '',
      modelo: '',
      ano: '',
      tipo: 'Repasse',
      quantidade: '',

      resumo: '',
      observacao: '',
    }
  )

  const refs = useRef<(HTMLInputElement | HTMLTextAreaElement | null)[]>([])

  function handleKeyDown(
    e: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>,
    index: number
  ) {
    if (e.key !== 'Enter') return

    e.preventDefault()
    refs.current[index + 1]?.focus()
  }

  return (
    <form className="caminhao-form">

      {/* Marca */}
      <input
       ref={(el) => {
        refs.current[0] = el
      }}
      
        placeholder="Marca"
        value={form.marca}
        onChange={(e) => setForm({ ...form, marca: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 0)}
      />

      {/* Modelo */}
      <input
       ref={(el) => {
        refs.current[1] = el
      }}
      
        placeholder="Modelo"
        value={form.modelo}
        onChange={(e) => setForm({ ...form, modelo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 1)}
      />

      {/* Ano */}
      <input
       ref={(el) => {
        refs.current[2] = el
      }}
      
        placeholder="Ano"
        value={form.ano}
        onChange={(e) => setForm({ ...form, ano: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 2)}
      />

      {/* Tipo */}
      <input
    ref={(el) => {
      refs.current[3] = el
    }}
    
        placeholder="Tipo (ex: Repasse)"
        value={form.tipo}
        onChange={(e) => setForm({ ...form, tipo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 3)}
      />


<input
  ref={(el) => {
    refs.current[4] = el
  }}
  type="text"
  inputMode="numeric"
  pattern="[0-9]*"
  placeholder="Quantidade"
  value={form.quantidade}
  onChange={(e) => {
    const value = e.target.value
    if (/^\d*$/.test(value)) {
      setForm({ ...form, quantidade: value })
    }
  }}
  onKeyDown={(e) => handleKeyDown(e, 4)}
/>


      {/* Resumo */}
      <textarea
       ref={(el) => {
        refs.current[5] = el
      }}
      
        placeholder="Resumo"
        value={form.resumo}
        onChange={(e) => setForm({ ...form, resumo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 4)}
      />

      {/* Observações */}
      <textarea
       ref={(el) => {
        refs.current[6] = el
      }}
      
        placeholder="Observações"
        value={form.observacao}
        onChange={(e) => setForm({ ...form, observacao: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, 5)}
      />

      <button
        type="button"
        className="btn-primary"
        onClick={() => onSave(form)}
      >
        Salvar caminhão
      </button>
    </form>
  )
}
