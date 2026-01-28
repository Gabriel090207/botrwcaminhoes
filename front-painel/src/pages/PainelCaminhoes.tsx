import { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import { DashboardCard } from '../components/DashboardCard'
import { ConversasChart } from '../components/ConversasChart'

interface DashboardData {
  conversasHoje: number
  emAndamento: number
  transferidas: number
  statusBot: string
}

export function PainelCaminhoes() {
  const [dados, setDados] = useState<DashboardData | null>(null)

  useEffect(() => {
    fetch('https://botrwcaminhoes.onrender.com/dashboard')
      .then(res => res.json())
      .then(data => setDados(data))
      .catch(err => {
        console.error('Erro ao carregar dashboard', err)
      })
  }, [])

  return (
    <Layout>
      <div className="dashboard-grid">
        <DashboardCard
          title="Conversas iniciadas hoje"
          value={dados ? String(dados.conversasHoje) : '—'}
          subtitle="Últimas 24h"
        />

        <DashboardCard
          title="Conversas em andamento"
          value={dados ? String(dados.emAndamento) : '—'}
        />

        <DashboardCard
          title="Conversas transferidas"
          value={dados ? String(dados.transferidas) : '—'}
        />

        <DashboardCard
          title="Status do Bot"
          value={dados ? dados.statusBot : '—'}
          subtitle="Funcionando normalmente"
        />
      </div>

      <ConversasChart />
    </Layout>
  )
}
