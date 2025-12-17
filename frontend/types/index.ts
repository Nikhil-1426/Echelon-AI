export interface Anomaly {
  metric: string
  severity: number
  explanation: string
}

export interface Diagnosis {
  partId: string
  partName: string
  confidence: number
  severityLevel: 'low' | 'medium' | 'high'
  estimatedTimeToFailure: number
}

export interface Schedule {
  workshopId: string
  workshopName: string
  slotTime: string
  priorityTag: 'low' | 'medium' | 'high'
}

export interface Feedback {
  customerRating: number
  diagnosisCorrect: boolean
  repairTimeHours: number
}

export interface VehicleData {
  vehicleId: string
  model: string
  customerId: string
  status: 'monitoring' | 'anomaly_detected' | 'scheduled' | 'serviced'
  anomalies: Anomaly[]
  diagnosis: Diagnosis | null
  schedule: Schedule | null
  feedback: Feedback | null
}

