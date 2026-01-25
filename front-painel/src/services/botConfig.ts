import { doc, setDoc, getDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase'

const BOT_DOC_ID = 'config'

export async function salvarPrompt(prompt: string) {
    await setDoc(
      doc(db, 'bot_config', BOT_DOC_ID),
      {
        promptBase: prompt,
        ativo: false,
        ultimaAtualizacao: serverTimestamp(),
      },
      { merge: true }
    )
  }
  
  export async function carregarPrompt(): Promise<string | null> {
    const snap = await getDoc(doc(db, 'bot_config', BOT_DOC_ID))
  
    if (!snap.exists()) return null
  
    const data = snap.data()
  
    if (data.ativo !== true) return null
  
    return data.promptBase || null
  }
  
  export async function aplicarPrompt() {
    await setDoc(
      doc(db, 'bot_config', 'config'),
      {
        ativo: true,
        ultimaAtualizacao: serverTimestamp(),
      },
      { merge: true }
    )
  }
  