import '../styles/dashboard-card.css'

interface DashboardCardProps {
  title: string
  value: string
  subtitle?: string
}

export function DashboardCard({ title, value, subtitle }: DashboardCardProps) {
  return (
    <div className="dashboard-card">
      <span className="card-title">{title}</span>
      <strong className="card-value">{value}</strong>
      {subtitle && <small className="card-subtitle">{subtitle}</small>}
    </div>
  )
}
