'use client'

import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#FFBE00', '#E6A800', '#FFD700', '#FFA500']

interface StatsData {
  totalVehicles: number
  anomaliesDetected: number
  scheduled: number
  serviced: number
  diagnosisAccuracy: number
  avgRating: number
  partFailures: Record<string, number>
  severityDistribution: Record<string, number>
}

export default function StatsOverview() {
  const [stats, setStats] = useState<StatsData>({
    totalVehicles: 0,
    anomaliesDetected: 0,
    scheduled: 0,
    serviced: 0,
    diagnosisAccuracy: 0,
    avgRating: 0,
    partFailures: {},
    severityDistribution: {},
  })
  const [manufacturingInsights, setManufacturingInsights] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch stats
        const statsResponse = await fetch('/api/stats')
        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          setStats({
            totalVehicles: statsData.totalVehicles || 0,
            anomaliesDetected: statsData.anomaliesDetected || 0,
            scheduled: statsData.scheduled || 0,
            serviced: statsData.serviced || 0,
            diagnosisAccuracy: statsData.diagnosisAccuracy || 0,
            avgRating: statsData.avgRating || 0,
            partFailures: statsData.partFailures || {},
            severityDistribution: statsData.severityDistribution || {},
          })
        }

        // Fetch manufacturing insights
        const mfgResponse = await fetch('/api/manufacturing')
        if (mfgResponse.ok) {
          const mfgData = await mfgResponse.json()
          setManufacturingInsights(mfgData.insights || [])
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  // Transform data for charts
  const partFailureData = Object.entries(stats.partFailures).map(([name, failures]) => ({
    name,
    failures,
  }))

  const severityDistribution = Object.entries(stats.severityDistribution).map(([name, value]) => ({
    name,
    value: value as number,
  }))

  // Mock trend data (could be enhanced with historical API endpoint)
  const anomalyTrendData = [
    { date: 'Mon', anomalies: Math.floor(stats.anomaliesDetected * 0.8) },
    { date: 'Tue', anomalies: Math.floor(stats.anomaliesDetected * 0.9) },
    { date: 'Wed', anomalies: Math.floor(stats.anomaliesDetected * 0.85) },
    { date: 'Thu', anomalies: stats.anomaliesDetected },
    { date: 'Fri', anomalies: Math.floor(stats.anomaliesDetected * 0.95) },
    { date: 'Sat', anomalies: Math.floor(stats.anomaliesDetected * 0.7) },
    { date: 'Sun', anomalies: Math.floor(stats.anomaliesDetected * 0.75) },
  ]

  // Workshop performance (mock for now, could be enhanced)
  const workshopPerformance = [
    { workshop: 'City Central', avgRating: stats.avgRating, services: Math.floor(stats.scheduled * 0.4) },
    { workshop: 'Northside', avgRating: stats.avgRating * 0.95, services: Math.floor(stats.scheduled * 0.3) },
    { workshop: 'Express South', avgRating: stats.avgRating * 0.98, services: Math.floor(stats.scheduled * 0.3) },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-ey-yellow"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-ey-yellow mb-2">Analytics & Insights</h2>
        <p className="text-gray-400">Manufacturing intelligence and performance metrics</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-ey-gray-light border-2 border-ey-yellow rounded-lg p-6">
          <p className="text-sm text-gray-400 mb-1">Diagnosis Accuracy</p>
          <p className="text-3xl font-bold text-ey-yellow">{stats.diagnosisAccuracy.toFixed(1)}%</p>
          <p className="text-xs text-green-400 mt-2">Based on feedback</p>
        </div>
        <div className="bg-ey-gray-light border-2 border-ey-yellow rounded-lg p-6">
          <p className="text-sm text-gray-400 mb-1">Total Vehicles</p>
          <p className="text-3xl font-bold text-ey-yellow">{stats.totalVehicles}</p>
          <p className="text-xs text-gray-400 mt-2">Fleet size</p>
        </div>
        <div className="bg-ey-gray-light border-2 border-ey-yellow rounded-lg p-6">
          <p className="text-sm text-gray-400 mb-1">Customer Satisfaction</p>
          <p className="text-3xl font-bold text-ey-yellow">{stats.avgRating.toFixed(1)}</p>
          <p className="text-xs text-gray-400 mt-2">out of 5.0</p>
        </div>
        <div className="bg-ey-gray-light border-2 border-ey-yellow rounded-lg p-6">
          <p className="text-sm text-gray-400 mb-1">Services Completed</p>
          <p className="text-3xl font-bold text-ey-yellow">{stats.serviced}</p>
          <p className="text-xs text-green-400 mt-2">With feedback</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Anomaly Trend */}
        <div className="bg-ey-gray-light rounded-lg p-6 border-2 border-ey-gray">
          <h3 className="text-xl font-semibold text-ey-yellow mb-4">Anomaly Detection Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={anomalyTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="date" stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #FFBE00', color: '#fff' }}
                labelStyle={{ color: '#FFBE00' }}
              />
              <Line
                type="monotone"
                dataKey="anomalies"
                stroke="#FFBE00"
                strokeWidth={3}
                dot={{ fill: '#FFBE00', r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Distribution */}
        <div className="bg-ey-gray-light rounded-lg p-6 border-2 border-ey-gray">
          <h3 className="text-xl font-semibold text-ey-yellow mb-4">Severity Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={severityDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {severityDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #FFBE00', color: '#fff' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Part Failure Frequency */}
        <div className="bg-ey-gray-light rounded-lg p-6 border-2 border-ey-gray">
          <h3 className="text-xl font-semibold text-ey-yellow mb-4">Part Failure Frequency</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={partFailureData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #FFBE00', color: '#fff' }}
                labelStyle={{ color: '#FFBE00' }}
              />
              <Bar dataKey="failures" fill="#FFBE00" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Workshop Performance */}
        <div className="bg-ey-gray-light rounded-lg p-6 border-2 border-ey-gray">
          <h3 className="text-xl font-semibold text-ey-yellow mb-4">Workshop Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={workshopPerformance}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="workshop" stroke="#999" />
              <YAxis yAxisId="left" stroke="#999" />
              <YAxis yAxisId="right" orientation="right" stroke="#999" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #FFBE00', color: '#fff' }}
                labelStyle={{ color: '#FFBE00' }}
              />
              <Bar yAxisId="left" dataKey="avgRating" fill="#FFBE00" name="Avg Rating" />
              <Bar yAxisId="right" dataKey="services" fill="#E6A800" name="Services" />
              <Legend />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Manufacturing Insights Table */}
      <div className="bg-ey-gray-light rounded-lg p-6 border-2 border-ey-gray">
        <h3 className="text-xl font-semibold text-ey-yellow mb-4">Recent Manufacturing Insights</h3>
        <div className="overflow-x-auto">
          {manufacturingInsights.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <p>No manufacturing insights available yet.</p>
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-ey-gray">
                  <th className="text-left py-3 px-4 text-ey-yellow">Vehicle ID</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Model</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Failed Part</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Workshop</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Repair Time</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Diagnosis</th>
                  <th className="text-left py-3 px-4 text-ey-yellow">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {manufacturingInsights.slice(0, 10).map((row: any, idx: number) => (
                  <tr key={idx} className="border-b border-ey-gray hover:bg-ey-gray">
                    <td className="py-3 px-4">{row.vehicle_id || 'N/A'}</td>
                    <td className="py-3 px-4">{row.model || 'N/A'}</td>
                    <td className="py-3 px-4">{row.failure_part_name || 'N/A'}</td>
                    <td className="py-3 px-4">{row.workshop_id || 'N/A'}</td>
                    <td className="py-3 px-4">{row.repair_time_hours?.toFixed(1) || 'N/A'}h</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${
                        row.diagnosis_correct ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {row.diagnosis_correct ? '✓ Correct' : '✗ Incorrect'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-400">
                      {row.timestamp ? new Date(row.timestamp).toLocaleString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
