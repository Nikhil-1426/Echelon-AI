'use client'

import { useState, useEffect } from 'react'

interface Stats {
  totalVehicles: number
  anomaliesDetected: number
  scheduled: number
  serviced: number
}

export default function CurrentStateSummary() {
  const [stats, setStats] = useState<Stats>({
    totalVehicles: 0,
    anomaliesDetected: 0,
    scheduled: 0,
    serviced: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats')
        if (!response.ok) {
          throw new Error('Failed to fetch stats')
        }
        const data = await response.json()
        setStats({
          totalVehicles: data.totalVehicles || 0,
          anomaliesDetected: data.anomaliesDetected || 0,
          scheduled: data.scheduled || 0,
          serviced: data.serviced || 0,
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
    const interval = setInterval(fetchStats, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-ey-gray-light border-l-4 border-ey-gray p-6 rounded animate-pulse">
            <div className="h-4 bg-ey-gray rounded w-24 mb-2"></div>
            <div className="h-8 bg-ey-gray rounded w-16"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-ey-gray-light border-l-4 border-ey-yellow p-6 rounded">
        <h3 className="text-lg font-semibold text-ey-yellow mb-2">Active Vehicles</h3>
        <p className="text-3xl font-bold">{stats.totalVehicles}</p>
        <p className="text-sm text-gray-400 mt-2">Total fleet size</p>
      </div>
      <div className="bg-ey-gray-light border-l-4 border-red-500 p-6 rounded">
        <h3 className="text-lg font-semibold text-red-400 mb-2">Anomalies Detected</h3>
        <p className="text-3xl font-bold">{stats.anomaliesDetected}</p>
        <p className="text-sm text-gray-400 mt-2">Requiring attention</p>
      </div>
      <div className="bg-ey-gray-light border-l-4 border-green-500 p-6 rounded">
        <h3 className="text-lg font-semibold text-green-400 mb-2">Services Scheduled</h3>
        <p className="text-3xl font-bold">{stats.scheduled}</p>
        <p className="text-sm text-gray-400 mt-2">Active schedules</p>
      </div>
    </div>
  )
}

