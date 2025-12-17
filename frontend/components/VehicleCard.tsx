'use client'

import { VehicleData } from '../types'

interface VehicleCardProps {
  vehicle: VehicleData
  isSelected: boolean
  onSelect: () => void
}

export default function VehicleCard({ vehicle, onSelect, isSelected }: VehicleCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'anomaly_detected':
        return 'bg-red-500'
      case 'scheduled':
        return 'bg-yellow-500'
      case 'monitoring':
        return 'bg-green-500'
      default:
        return 'bg-gray-500'
    }
  }

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'anomaly_detected':
        return 'Anomaly Detected'
      case 'scheduled':
        return 'Scheduled'
      case 'monitoring':
        return 'Normal'
      default:
        return status
    }
  }

  return (
    <div
      onClick={onSelect}
      className={`bg-ey-gray-light border-2 rounded-lg p-6 cursor-pointer transition-all hover:border-ey-yellow ${
        isSelected ? 'border-ey-yellow shadow-lg shadow-ey-yellow/20' : 'border-ey-gray'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-ey-yellow">{vehicle.vehicleId}</h3>
          <p className="text-sm text-gray-400">{vehicle.model}</p>
          <p className="text-xs text-gray-500 mt-1">Customer: {vehicle.customerId}</p>
        </div>
        <div className={`w-3 h-3 rounded-full ${getStatusColor(vehicle.status)}`}></div>
      </div>

      {/* Status Badge */}
      <div className="mb-4">
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
          vehicle.status === 'anomaly_detected' ? 'bg-red-500/20 text-red-400' :
          vehicle.status === 'scheduled' ? 'bg-yellow-500/20 text-yellow-400' :
          'bg-green-500/20 text-green-400'
        }`}>
          {getStatusLabel(vehicle.status)}
        </span>
      </div>

      {/* Anomalies */}
      {vehicle.anomalies.length > 0 && (
        <div className="mb-4">
          <p className="text-sm font-semibold text-gray-300 mb-2">
            Anomalies: {vehicle.anomalies.length}
          </p>
          <div className="space-y-2">
            {vehicle.anomalies.slice(0, 2).map((anomaly, idx) => (
              <div key={idx} className="bg-ey-gray p-2 rounded text-xs">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-ey-yellow font-medium">{anomaly.metric}</span>
                  <span className="text-red-400 font-bold">
                    {(anomaly.severity * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-gray-400 text-xs truncate">{anomaly.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Diagnosis */}
      {vehicle.diagnosis && (
        <div className="mb-4 p-3 bg-ey-gray rounded border-l-4 border-ey-yellow">
          <p className="text-sm font-semibold text-ey-yellow mb-1">Diagnosis</p>
          <p className="text-sm text-white">{vehicle.diagnosis.partName}</p>
          <div className="flex justify-between mt-2 text-xs">
            <span className="text-gray-400">Confidence:</span>
            <span className="text-white font-semibold">
              {(vehicle.diagnosis.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="flex justify-between mt-1 text-xs">
            <span className="text-gray-400">Time to Failure:</span>
            <span className="text-red-400 font-semibold">
              {vehicle.diagnosis.estimatedTimeToFailure} days
            </span>
          </div>
        </div>
      )}

      {/* Schedule */}
      {vehicle.schedule && (
        <div className="mb-4 p-3 bg-ey-gray rounded">
          <p className="text-sm font-semibold text-ey-yellow mb-1">Scheduled Service</p>
          <p className="text-sm text-white">{vehicle.schedule.workshopName}</p>
          <p className="text-xs text-gray-400 mt-1">
            {new Date(vehicle.schedule.slotTime).toLocaleString()}
          </p>
          <span className={`inline-block mt-2 px-2 py-1 rounded text-xs ${
            vehicle.schedule.priorityTag === 'high' ? 'bg-red-500/20 text-red-400' :
            vehicle.schedule.priorityTag === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
            'bg-green-500/20 text-green-400'
          }`}>
            {vehicle.schedule.priorityTag.toUpperCase()} Priority
          </span>
        </div>
      )}

      {/* Feedback */}
      {vehicle.feedback && (
        <div className="p-3 bg-ey-gray rounded">
          <p className="text-sm font-semibold text-ey-yellow mb-1">Service Feedback</p>
          <div className="flex items-center space-x-2">
            <span className="text-2xl text-ey-yellow">★</span>
            <span className="text-lg font-bold">{vehicle.feedback.customerRating}</span>
            <span className="text-xs text-gray-400 ml-auto">
              {vehicle.feedback.diagnosisCorrect ? '✓ Correct' : '✗ Incorrect'}
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-1">
            Repair Time: {vehicle.feedback.repairTimeHours}h
          </p>
        </div>
      )}

      {vehicle.anomalies.length === 0 && !vehicle.diagnosis && (
        <div className="text-center py-4 text-gray-500 text-sm">
          All systems normal
        </div>
      )}
    </div>
  )
}

