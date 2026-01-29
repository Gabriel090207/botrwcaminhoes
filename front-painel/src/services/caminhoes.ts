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
import { ref, uploadBytes, getDownloadURL, listAll, deleteObject } from 'firebase/storage'
import { db, storage } from './firebase'
import type { Caminhao } from '../components/CaminhaoForm'

const COLLECTION = 'caminhoes'

/**
 * Upload das imagens do caminhão para o Firebase Storage
 */
async function uploadImagensCaminhao(
  caminhaoId: string,
  imagens: File[]
): Promise<string[]> {
  const urls: string[] = []

  for (let i = 0; i < imagens.length; i++) {
    const file = imagens[i]

    const imageRef = ref(
      storage,
      `caminhoes/${caminhaoId}/${i + 1}.jpg`
    )

    await uploadBytes(imageRef, file)
    const url = await getDownloadURL(imageRef)
    urls.push(url)
  }

  return urls
}

/**
 * Criar caminhão
 */
export async function criarCaminhao(caminhao: Caminhao): Promise<void> {
  const refDoc = doc(db, COLLECTION, caminhao.id)

  const { imagens, ...dados } = caminhao

  let imagensUrls: string[] = []

  if (imagens && imagens.length > 0) {
    imagensUrls = await uploadImagensCaminhao(caminhao.id, imagens)
  }

  await setDoc(refDoc, {
    ...dados,
    imagens: imagensUrls,
    ativo: true,
    criadoEm: serverTimestamp(),
  })
}

/**
 * Listar caminhões ativos
 */
export async function listarCaminhoes(): Promise<Caminhao[]> {
  const q = query(
    collection(db, COLLECTION),
    where('ativo', '==', true)
  )

  const snap = await getDocs(q)

  return snap.docs.map(docSnap => ({
    id: docSnap.id,
    ...(docSnap.data() as Omit<Caminhao, 'id'>),
  }))
}

/**
 * Remover caminhão (soft delete)
 * Opcional: também remove imagens do Storage
 */
export async function removerCaminhao(id: string): Promise<void> {
  const refDoc = doc(db, COLLECTION, id)

  // soft delete
  await updateDoc(refDoc, { ativo: false })

  // 🔥 opcional: apagar imagens do storage
  try {
    const folderRef = ref(storage, `caminhoes/${id}`)
    const files = await listAll(folderRef)

    await Promise.all(
      files.items.map(fileRef => deleteObject(fileRef))
    )
  } catch (e) {
    console.warn('Não foi possível remover imagens do storage:', e)
  }
}
