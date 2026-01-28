import { useEffect, useState } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import '../styles/conversas-chart.css'

interface ConversaHora {
  hora: string
  conversas: number
}

export function ConversasChart() {
  const [data, setData] = useState<ConversaHora[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('https://botrwcaminhoes.onrender.com/dashboard/conversas-hora')
      .then(res => res.json())
      .then(dados => {
        const normalizado = dados
          .map((item: any) => ({
            hora: item.hora,
            conversas: Number(item.conversas),
          }))
          .sort((a: any, b: any) => Number(a.hora) - Number(b.hora))

        setData(normalizado)
        setLoading(false)
      })
      .catch(err => {
        console.error('Erro ao carregar gráfico', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="chart-container">
        <h3>Pico de conversas por horário</h3>
        <p>Carregando gráfico...</p>
      </div>
    )
  }

  return (
    <div className="chart-container">
      <h3>Pico de conversas por horário</h3>

      <ResponsiveContainer width="100%" height={420}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="blueGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--blue-secondary)" stopOpacity={0.6} />
              <stop offset="100%" stopColor="var(--blue-secondary)" stopOpacity={0.05} />
            </linearGradient>
          </defs>

          <CartesianGrid stroke="var(--chart-grid)" vertical={false} />

          {/* EIXO X → HORÁRIO */}
          <XAxis
            dataKey="hora"
            stroke="var(--chart-axis)"
            tickLine={false}
            axisLine={false}
          />

          {/* EIXO Y → QUANTIDADE */}
          <YAxis
            stroke="var(--chart-axis-muted)"
            tickLine={false}
            axisLine={false}
            allowDecimals={false}
            width={35}
          />

          <Tooltip
  formatter={(value) => [`${value} conversas`, '']}
  labelFormatter={(label) => `Horário: ${label}h`}
  contentStyle={{
    backgroundColor: 'var(--chart-tooltip-bg)',
    border: '1px solid var(--chart-tooltip-border)',
    borderRadius: '8px',
    color: 'var(--chart-tooltip-text)',
    fontSize: '13px',
  }}
/>


          <Area
            type="monotone"
            dataKey="conversas"
            stroke="var(--blue-secondary)"
            strokeWidth={2.5}
            fill="url(#blueGradient)"
            dot={false}
            activeDot={{ r: 5 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
