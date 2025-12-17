'use client'

import { useState, useEffect } from 'react'
import VehicleCard from './VehicleCard'
import { VehicleData } from '../types'

export default function VehicleDashboard() {
  const [vehicles, setVehicles] = useState<VehicleData[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedVehicle, setSelectedVehicle] = useState<string | null>(null)

  useEffect(() => {
    const fetchVehicles = async () => {
      setLoading(true)
      try {
        const response = await fetch('/api/vehicles')
        if (!response.ok) {
          throw new Error('Failed to fetch vehicles')
        }
        const data = await response.json()
        
        // Transform API response to component format
        const vehiclesData: VehicleData[] = data.vehicles.map((v: any) => ({
          vehicleId: v.vehicleId,
          model: v.model,
          customerId: v.customerId,
          status: v.status,
          anomalies: v.anomalies || [],
          diagnosis: v.diagnosis,
          schedule: v.schedule,
          feedback: v.feedback,
        }))
        
        setVehicles(vehiclesData)
      } catch (error) {
        console.error('Error fetching vehicles:', error)
        // Set empty array on error to show empty state
        setVehicles([])
      } finally {
        setLoading(false)
      }
    }

    fetchVehicles()
    // Refresh every 30 seconds
    const interval = setInterval(fetchVehicles, 30000)
    return () => clearInterval(interval)
  }, [])

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
        <h2 className="text-3xl font-bold text-ey-yellow mb-2">Vehicle Fleet Monitoring</h2>
        <p className="text-gray-400">Real-time anomaly detection and predictive maintenance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {vehicles.map((vehicle) => (
          <VehicleCard
            key={vehicle.vehicleId}
            vehicle={vehicle}
            isSelected={selectedVehicle === vehicle.vehicleId}
            onSelect={() => setSelectedVehicle(
              selectedVehicle === vehicle.vehicleId ? null : vehicle.vehicleId
            )}
          />
        ))}
      </div>

      {vehicles.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p>No vehicles found. Start monitoring to see vehicle data.</p>
        </div>
      )}
    </div>
  )
}

