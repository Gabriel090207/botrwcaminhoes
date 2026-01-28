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

const data = [
  { hora: '06h', conversas: 2 },
  { hora: '08h', conversas: 5 },
  { hora: '10h', conversas: 12 },
  { hora: '12h', conversas: 18 },
  { hora: '14h', conversas: 14 },
  { hora: '16h', conversas: 9 },
  { hora: '18h', conversas: 6 },
  { hora: '20h', conversas: 3 },
]

export function ConversasChart() {
  return (
    <div className="chart-container">
      <h3>Pico de conversas por horário</h3>

      <ResponsiveContainer width="100%" height={420}>
        <AreaChart data={data}>
          {/* Gradiente azul */}
          <defs>
            <linearGradient id="blueGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--blue-secondary)" stopOpacity={0.6} />
              <stop offset="100%" stopColor="var(--blue-secondary)" stopOpacity={0.05} />
            </linearGradient>
          </defs>

          {/* Grid sutil */}
          <CartesianGrid
            stroke="var(--chart-grid)"
            vertical={false}
          />

          {/* Eixo X */}
          <XAxis
            dataKey="hora"
            stroke="var(--chart-axis)"
            tickLine={false}
            axisLine={false}
            padding={{ left: 15, right: 0 }}
          />

          {/* Eixo Y */}
          <YAxis
            stroke="var(--chart-axis-muted)"
            tickLine={false}
            axisLine={false}
            width={30}
            tickMargin={6}
          />

          {/* Tooltip */}
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--chart-tooltip-bg)',
              border: '1px solid var(--chart-tooltip-border)',
              borderRadius: '8px',
              color: 'var(--chart-tooltip-text)',
              fontSize: '13px',
            }}
            labelStyle={{ color: 'var(--chart-tooltip-label)' }}
          />

          {/* Área + linha */}
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
