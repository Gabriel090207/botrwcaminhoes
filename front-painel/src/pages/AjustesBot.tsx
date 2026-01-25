import { useState } from 'react'
import { Layout } from '../components/Layout'
import '../styles/ajustes-bot.css'

import { salvarPrompt, carregarPrompt, aplicarPrompt } from '../services/botConfig'
import { useEffect } from 'react'


interface Mensagem {
  id: string
  autor: 'admin' | 'bot'
  texto: string
}

export function AjustesBot() {

    const [ajusteAtivo, setAjusteAtivo] = useState(false)

    const [promptSalvo, setPromptSalvo] = useState('')



    useEffect(() => {
      async function carregar() {
        const prompt = await carregarPrompt()
        if (prompt) {
          setPromptSalvo(prompt)
        }
      }
    
      carregar()
    }, [])
    
      const [mensagens, setMensagens] = useState<Mensagem[]>([])


  const [texto, setTexto] = useState('')


  function gerarRespostaHumanizada(texto: string) {
    const msg = texto.toLowerCase()
  
    if (msg === 'oi' || msg === 'olá' || msg === 'ola') {
      return 'Olá! 😊 Me conta o que você espera do meu atendimento.'
    }
  
    if (msg.includes('educad')) {
      return 'Perfeito 👍 Vou manter um tom educado e respeitoso em todas as respostas.'
    }
  
    if (msg.includes('rápido') || msg.includes('rapido')) {
      return 'Certo! Vou priorizar respostas curtas e objetivas.'
    }
  
    if (msg.includes('cliente') && msg.includes('raiva')) {
      return 'Entendido. Em casos de clientes irritados, vou agir com calma e empatia.'
    }
  
    if (msg.includes('formal')) {
      return 'Ok! Vou adotar um tom mais formal nas conversas.'
    }
  
    if (msg.includes('informal')) {
      return 'Beleza 😄 Vou usar um tom mais leve e informal.'
    }
  
    return 'Entendi 👍 Pode me explicar um pouco mais ou dar um exemplo?'
  }
  

  function enviarMensagem() {
    if (!texto.trim()) return
  
    const mensagemAdmin: Mensagem = {
      id: crypto.randomUUID(),
      autor: 'admin',
      texto,
    }
  
    setMensagens(prev => [...prev, mensagemAdmin])
    setTexto('')
  
    const respostaBot = gerarRespostaHumanizada(texto)
  
    setTimeout(() => {
      setMensagens(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          autor: 'bot',
          texto: respostaBot,
        },
      ])
    }, 600)
  }
  

  function gerarPromptFinal() {
    return mensagens
      .filter(msg => msg.autor === 'admin')
      .map(msg => `- ${msg.texto}`)
      .join('\n')
  }
  
  async function aplicarAjustes() {
    const promptFinal = gerarPromptFinal()
  
    if (!promptFinal) return
  
    await salvarPrompt(promptFinal)
    await aplicarPrompt()
  
    setMensagens(prev => [
      ...prev,
      {
        id: crypto.randomUUID(),
        autor: 'bot',
        texto:
          '✅ Ajustes aplicados com sucesso. A partir de agora vou usar esse comportamento nas conversas.',
      },
    ])
  
    setAjusteAtivo(true)
  }
  
  
  
  return (
    <Layout>
      <div className="ajustes-bot-page">
       
        {promptSalvo && mensagens.length === 0 && (
   <h2>Ajustes do Bot</h2>
)}


        <div className="chat-box">
          {mensagens.map(msg => (
            <div
              key={msg.id}
              className={`chat-message ${msg.autor}`}
            >
              {msg.texto}
            </div>
          ))}
        </div>

        <div className="chat-input">
  <input
    placeholder="Explique como o bot deve responder..."
    value={texto}
    onChange={e => setTexto(e.target.value)}
    onKeyDown={e => e.key === 'Enter' && enviarMensagem()}
  />

  <button onClick={enviarMensagem}>
    Enviar
  </button>

  <button className="btn-primary" onClick={aplicarAjustes}>
    Aplicar ajustes
  </button>
</div>


{ajusteAtivo && (
  <p className="ajuste-ativo">

  </p>
)}


      </div>
    </Layout>
  )
}
