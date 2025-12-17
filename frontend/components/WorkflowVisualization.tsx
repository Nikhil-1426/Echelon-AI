'use client'

import { useState } from 'react'
import CurrentStateSummary from './CurrentStateSummary'

interface WorkflowStep {
  id: string
  name: string
  status: 'completed' | 'active' | 'pending'
  description: string
  data?: any
}

export default function WorkflowVisualization() {
  const [selectedStep, setSelectedStep] = useState<string | null>(null)

  const workflowSteps: WorkflowStep[] = [
    {
      id: 'ingest',
      name: 'Data Ingestion',
      status: 'completed',
      description: 'Telemetry data loaded and normalized',
      data: { points: 336, source: 'Excel Dataset' },
    },
    {
      id: 'anomaly',
      name: 'Anomaly Detection',
      status: 'completed',
      description: 'LSTM-based temporal anomaly detection',
      data: { anomaliesFound: 7, threshold: 0.05 },
    },
    {
      id: 'diagnosis',
      name: 'Diagnosis',
      status: 'completed',
      description: 'Part failure prediction and severity assessment',
      data: { part: 'Battery', severity: 'high', confidence: 0.75 },
    },
    {
      id: 'engagement',
      name: 'Customer Engagement',
      status: 'completed',
      description: 'Notification decision and message crafting',
      data: { notified: true, urgency: 'high' },
    },
    {
      id: 'scheduling',
      name: 'Workshop Scheduling',
      status: 'completed',
      description: 'FCFS + Priority-based slot allocation',
      data: { workshop: 'City Central Auto', priority: 'high' },
    },
    {
      id: 'feedback',
      name: 'Feedback Collection',
      status: 'active',
      description: 'Post-service feedback and validation',
      data: { rating: 4.83, correct: true },
    },
    {
      id: 'manufacturing',
      name: 'Manufacturing Insights',
      status: 'pending',
      description: 'OEM analytics payload generation',
      data: null,
    },
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✓'
      case 'active':
        return '⟳'
      case 'pending':
        return '○'
      default:
        return '○'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500 border-green-500'
      case 'active':
        return 'bg-ey-yellow border-ey-yellow animate-pulse'
      case 'pending':
        return 'bg-gray-500 border-gray-500'
      default:
        return 'bg-gray-500 border-gray-500'
    }
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-ey-yellow mb-2">Workflow Visualization</h2>
        <p className="text-gray-400">Real-time LangGraph workflow execution pipeline</p>
      </div>

      {/* Workflow Steps */}
      <div className="bg-ey-gray-light rounded-lg p-8">
        <div className="relative">
          {/* Connection Lines */}
          <div className="absolute top-12 left-0 right-0 h-0.5 bg-ey-gray" style={{ top: '48px' }}></div>
          
          <div className="flex justify-between items-start">
            {workflowSteps.map((step, index) => (
              <div key={step.id} className="flex flex-col items-center flex-1 relative">
                {/* Step Circle */}
                <div
                  onClick={() => setSelectedStep(selectedStep === step.id ? null : step.id)}
                  className={`w-24 h-24 rounded-full border-4 flex items-center justify-center cursor-pointer transition-all hover:scale-110 ${
                    getStatusColor(step.status)
                  } ${selectedStep === step.id ? 'ring-4 ring-ey-yellow ring-offset-2 ring-offset-ey-black' : ''}`}
                >
                  <span className="text-2xl font-bold text-ey-black">
                    {getStatusIcon(step.status)}
                  </span>
                </div>

                {/* Step Label */}
                <div className="mt-4 text-center">
                  <p className="text-sm font-semibold text-ey-yellow">{step.name}</p>
                  <p className="text-xs text-gray-400 mt-1">{step.description}</p>
                </div>

                {/* Step Data */}
                {selectedStep === step.id && step.data && (
                  <div className="absolute top-32 left-0 right-0 bg-ey-gray border-2 border-ey-yellow rounded-lg p-4 z-10">
                    <div className="text-xs space-y-1">
                      {Object.entries(step.data).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-gray-400 capitalize">{key}:</span>
                          <span className="text-white font-semibold">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Arrow */}
                {index < workflowSteps.length - 1 && (
                  <div className="absolute top-12 right-0 w-full h-0.5 bg-ey-gray">
                    <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-0 h-0 border-l-8 border-l-ey-gray border-t-4 border-t-transparent border-b-4 border-b-transparent"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <CurrentStateSummary />
    </div>
  )
}

