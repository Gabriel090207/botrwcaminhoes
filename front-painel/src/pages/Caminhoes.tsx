import { useState, useEffect } from 'react'
import { Layout } from '../components/Layout'
import { CaminhaoItem } from '../components/CaminhaoItem'
import { Modal } from '../components/Modal'
import { CaminhaoForm } from '../components/CaminhaoForm'
import type { Caminhao } from '../components/CaminhaoForm'
import { FiSearch } from 'react-icons/fi'


import '../styles/caminhoes.css'


import {
  criarCaminhao,
  atualizarCaminhao,
  listarCaminhoes,
  removerCaminhao as removerCaminhaoFirebase,
} from '../services/caminhoes'


export function Caminhoes() {
  const [caminhoes, setCaminhoes] = useState<Caminhao[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [editando, setEditando] = useState<Caminhao | null>(null)
  const [pesquisa, setPesquisa] = useState('')



  useEffect(() => {
    async function carregar() {
      const lista = await listarCaminhoes()
      setCaminhoes(lista)
    }
  
    carregar()
  }, [])
  

  async function salvarCaminhao(data: Caminhao) {

  try {

    console.log("SALVAR INICIADO", data)

    if (editando) {
      console.log("EDITANDO CAMINHÃO")
      await atualizarCaminhao(data)
    } else {
      console.log("CRIANDO CAMINHÃO")
      await criarCaminhao(data)
    }

    console.log("SALVOU NO FIREBASE")

    const lista = await listarCaminhoes()
    setCaminhoes(lista)

    setModalOpen(false)
    setEditando(null)

    console.log("MODAL FECHADO")

  } catch (erro) {
    console.error("ERRO AO SALVAR:", erro)
    alert("Erro ao salvar caminhão. Veja console.")
  }
}

  

  async function removerCaminhao(id: string) {
    await removerCaminhaoFirebase(id)
  
    const lista = await listarCaminhoes()
    setCaminhoes(lista)
  }

  const caminhoesFiltrados = caminhoes.filter(c => {
    const texto = pesquisa.toLowerCase()
  
    return (
      c.marca.toLowerCase().includes(texto) ||
      c.modelo.toLowerCase().includes(texto) ||
      c.ano.toLowerCase().includes(texto) ||
      c.tipo.toLowerCase().includes(texto)
    )
  })
  
  
  return (
    <Layout>
      <div className="caminhoes-page">
      <div className="caminhoes-header">
  <h2>Caminhões</h2>

  <div className="search-container">
  <span className="search-icon">
  <FiSearch />
</span>

<input
  type="text"
  placeholder="Pesquisar caminhão..."
  className="search-input"
  value={pesquisa}
  onChange={(e) => setPesquisa(e.target.value)}
/>

  </div>

  <button
    className="btn-primary"
    onClick={() => setModalOpen(true)}
  >
    Cadastrar caminhão
  </button>
</div>


        <div className="caminhoes-list">
        {caminhoesFiltrados.length === 0 && (
  <p className="empty">
    {pesquisa
      ? 'Nenhum caminhão encontrado'
      : 'Nenhum caminhão cadastrado'}
  </p>
)}

{caminhoesFiltrados.map(c => (
  <CaminhaoItem
    key={c.id}
    caminhao={c}
    onEdit={() => {
      setEditando(c)
      setModalOpen(true)
    }}
    onDelete={() => removerCaminhao(c.id)}
  />
))}

        </div>
      </div>

      <Modal
        title={editando ? 'Editar caminhão' : 'Cadastrar caminhão'}
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false)
          setEditando(null)
        }}
      >
        <CaminhaoForm
          initialData={editando || undefined}
          onSave={salvarCaminhao}
        />
      </Modal>
    </Layout>
  )
}
