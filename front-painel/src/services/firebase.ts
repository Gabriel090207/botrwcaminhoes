import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getStorage } from 'firebase/storage'



const firebaseConfig = {
    apiKey: "AIzaSyBmRtz1vbpTBC6uYiuBRNqd8PZvYst1N0Q",
    authDomain: "rwcaminhoes-bancodedados.firebaseapp.com",
    projectId: "rwcaminhoes-bancodedados",
    storageBucket: "rwcaminhoes-bancodedados.firebasestorage.app",
    messagingSenderId: "143133437473",
    appId: "1:143133437473:web:cfacb4e7af2b0a081dfd60",
    measurementId: "G-30LY01RSLB"
  };

const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
export const storage = getStorage(app)
