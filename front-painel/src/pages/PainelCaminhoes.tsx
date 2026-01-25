import { Layout } from '../components/Layout'
import { DashboardCard } from '../components/DashboardCard'
import { ConversasChart } from '../components/ConversasChart'

export function PainelCaminhoes() {
  return (
    <Layout>
      <div className="dashboard-grid">
        <DashboardCard title="Conversas iniciadas hoje" value="0" subtitle="Últimas 24h" />
        <DashboardCard title="Conversas em andamento" value="0" />
        <DashboardCard title="Conversas transferidas" value="0" />
        <DashboardCard title="Status do Bot" value="Ativo" subtitle="Funcionando normalmente" />
      </div>

      <ConversasChart />
    </Layout>
  )
}
