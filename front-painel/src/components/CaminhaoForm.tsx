import { useState, useRef } from 'react'
import '../styles/caminhao-form.css'
import { FiUploadCloud } from 'react-icons/fi'


export interface Caminhao {
  id: string
  marca: string
  modelo: string
  ano: string
  tipo: string
  quantidade: string

  tracao: string
  entreEixo: string

  valor: string

  resumo: string
  observacao: string

  imagens?: File[]
}

interface CaminhaoFormProps {
  initialData?: Caminhao
  onSave: (data: Caminhao) => void
}

export function CaminhaoForm({ initialData, onSave }: CaminhaoFormProps) {
  const [form, setForm] = useState<Caminhao>(() => {

  if (initialData) {
    return {
      ...initialData,
      imagens: []
    }
  }

  return {
    id: crypto.randomUUID(),
    marca: '',
    modelo: '',
    ano: '',
    tipo: 'Repasse',
    quantidade: '',
    tracao: '',
    entreEixo: '',
    valor: '',
    resumo: '',
    observacao: '',
    imagens: []
  }
})

  

  const [previews, setPreviews] = useState<string[]>([])

  // ===== REFS =====
  const marcaRef = useRef<HTMLInputElement | null>(null)
  const modeloRef = useRef<HTMLInputElement | null>(null)
  const anoRef = useRef<HTMLInputElement | null>(null)
  const tipoRef = useRef<HTMLInputElement | null>(null)
  const quantidadeRef = useRef<HTMLInputElement | null>(null)
  const tracaoRef = useRef<HTMLSelectElement | null>(null)
  const entreEixoRef = useRef<HTMLInputElement | null>(null)
  const valorRef = useRef<HTMLInputElement | null>(null)
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

  // ===== MÁSCARA R$ =====
  function formatarValor(valor: string) {
    const numero = valor.replace(/\D/g, '')
    const inteiro = (Number(numero) / 100).toFixed(2)
    return inteiro.replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  }

  function handleValorChange(e: React.ChangeEvent<HTMLInputElement>) {
    const somenteNumeros = e.target.value.replace(/\D/g, '')
    setForm({ ...form, valor: somenteNumeros })
  }

  // ===== IMAGENS =====
  function handleImageChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files) return

    const files = Array.from(e.target.files)
    setForm({ ...form, imagens: files })

    const urls = files.map((file) => URL.createObjectURL(file))
    setPreviews(urls)
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
        placeholder="Quantidade"
        inputMode="numeric"
        value={form.quantidade}
        onChange={(e) => {
          if (/^\d*$/.test(e.target.value)) {
            setForm({ ...form, quantidade: e.target.value })
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
        onKeyDown={(e) => handleKeyDown(e, valorRef)}
      />

      {/* Valor */}
      <input
        ref={valorRef}
        placeholder="Valor"
        value={form.valor ? `R$ ${formatarValor(form.valor)}` : ''}
        onChange={handleValorChange}
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

      {/* Upload de imagens */}
      <div className="upload-box">
        <label htmlFor="imagens">
          <div className="upload-placeholder">
  <FiUploadCloud size={36} />
  <p>Clique para adicionar fotos do caminhão</p>
</div>

        </label>

        <input
          id="imagens"
          type="file"
          multiple
          accept="image/*"
          onChange={handleImageChange}
          hidden
        />
      </div>

      {/* Preview */}
      <div className="preview-container">
        {previews.map((src, index) => (
          <img key={index} src={src} alt="Preview" />
        ))}
      </div>

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
