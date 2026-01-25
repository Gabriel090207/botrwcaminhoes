import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { PainelCaminhoes } from './pages/PainelCaminhoes'
import { Caminhoes } from './pages/Caminhoes'
import { AjustesBot } from './pages/AjustesBot'


export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PainelCaminhoes />} />
        <Route path="/caminhoes" element={<Caminhoes />} />
        <Route path="/ajustes" element={<AjustesBot />} />

      </Routes>
    </BrowserRouter>
  )
}
