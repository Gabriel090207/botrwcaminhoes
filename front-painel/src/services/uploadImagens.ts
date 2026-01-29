import { ref, uploadBytes, getDownloadURL } from 'firebase/storage'
import { storage } from './firebase'

export async function uploadImagensCaminhao(
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
