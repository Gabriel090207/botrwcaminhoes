import {
    collection,
    doc,
    setDoc,
    getDocs,
    updateDoc,
    serverTimestamp,
    query,
    where,
  } from 'firebase/firestore'
  import { db } from './firebase'
  import type { Caminhao } from '../components/CaminhaoForm'
  
  const COLLECTION = 'caminhoes'
  
  export async function criarCaminhao(caminhao: Caminhao): Promise<void> {
    const ref = doc(db, COLLECTION, caminhao.id)
  
    await setDoc(ref, {
      ...caminhao,
      ativo: true,
      criadoEm: serverTimestamp(),
    })
  }
  
  export async function listarCaminhoes(): Promise<Caminhao[]> {
    const q = query(
      collection(db, COLLECTION),
      where('ativo', '==', true)
    )
  
    const snap = await getDocs(q)
  
    return snap.docs.map(doc => ({
      id: doc.id,
      ...(doc.data() as Omit<Caminhao, 'id'>),
    }))
  }
  
  export async function removerCaminhao(id: string): Promise<void> {
    const ref = doc(db, COLLECTION, id)
    await updateDoc(ref, { ativo: false })
  }
  