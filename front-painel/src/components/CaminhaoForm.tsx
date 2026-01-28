import { useState, useRef } from 'react'
import '../styles/caminhao-form.css'

export interface Caminhao {
  id: string
  marca: string
  modelo: string
  ano: string
  tipo: string
  quantidade: string

  tracao: string
  entreEixo: string

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

      tracao: '',
      entreEixo: '',

      resumo: '',
      observacao: '',
    }
  )

  // ===== REFS =====
  const marcaRef = useRef<HTMLInputElement | null>(null)
  const modeloRef = useRef<HTMLInputElement | null>(null)
  const anoRef = useRef<HTMLInputElement | null>(null)
  const tipoRef = useRef<HTMLInputElement | null>(null)
  const quantidadeRef = useRef<HTMLInputElement | null>(null)
  const tracaoRef = useRef<HTMLSelectElement | null>(null)
  const entreEixoRef = useRef<HTMLInputElement | null>(null)
  const resumoRef = useRef<HTMLTextAreaElement | null>(null)
  const observacaoRef = useRef<HTMLTextAreaElement | null>(null)

  function handleKeyDown(
    e: React.KeyboardEvent,
    nextRef?: { current: HTMLElement | null }
  ) {
    if (e.key !== 'Enter') return
    e.preventDefault()
    nextRef?.current?.focus()
  }

  return (
    <form className="caminhao-form">
      {/* Marca */}
      <input
        ref={marcaRef}
        placeholder="Marca"
        value={form.marca}
        onChange={(e) => setForm({ ...form, marca: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, modeloRef)}
      />

      {/* Modelo */}
      <input
        ref={modeloRef}
        placeholder="Modelo"
        value={form.modelo}
        onChange={(e) => setForm({ ...form, modelo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, anoRef)}
      />

      {/* Ano */}
      <input
        ref={anoRef}
        placeholder="Ano"
        value={form.ano}
        onChange={(e) => setForm({ ...form, ano: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, tipoRef)}
      />

      {/* Tipo */}
      <input
        ref={tipoRef}
        placeholder="Tipo (ex: Repasse)"
        value={form.tipo}
        onChange={(e) => setForm({ ...form, tipo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, quantidadeRef)}
      />

      {/* Quantidade */}
      <input
        ref={quantidadeRef}
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
        onKeyDown={(e) => handleKeyDown(e, tracaoRef)}
      />

      {/* Tração */}
      <select
        ref={tracaoRef}
        value={form.tracao}
        onChange={(e) => setForm({ ...form, tracao: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, entreEixoRef)}
      >
        <option value="">Tração</option>
        <option value="4x2">4x2 (Toco)</option>
        <option value="6x2">6x2 (Trucado)</option>
        <option value="6x4">6x4 (Traçado)</option>
        <option value="8x2">8x2 (Bitruck)</option>
      </select>

      {/* Entre-eixo */}
      <input
        ref={entreEixoRef}
        placeholder="Entre-eixo (ex: 3.20)"
        value={form.entreEixo}
        onChange={(e) => setForm({ ...form, entreEixo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, resumoRef)}
      />

      {/* Resumo */}
      <textarea
        ref={resumoRef}
        placeholder="Resumo"
        value={form.resumo}
        onChange={(e) => setForm({ ...form, resumo: e.target.value })}
        onKeyDown={(e) => handleKeyDown(e, observacaoRef)}
      />

      {/* Observações */}
      <textarea
        ref={observacaoRef}
        placeholder="Observações"
        value={form.observacao}
        onChange={(e) => setForm({ ...form, observacao: e.target.value })}
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
