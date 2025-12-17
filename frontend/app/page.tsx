'use client'

import { useState, useEffect } from 'react'
import VehicleDashboard from '../components/VehicleDashboard'
import WorkflowVisualization from '../components/WorkflowVisualization'
import StatsOverview from '../components/StatsOverview'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'workflow' | 'stats'>('dashboard')

  return (
    <main className="min-h-screen bg-ey-black text-white">
      {/* Header */}
      <header className="bg-ey-gray border-b-2 border-ey-yellow">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-ey-yellow rounded-lg flex items-center justify-center">
                <span className="text-ey-black font-bold text-xl">EY</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-ey-yellow">Agentic AI</h1>
                <p className="text-sm text-gray-400">Automotive Aftersales Predictive Maintenance</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm">System Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-ey-gray-light border-b border-ey-gray">
        <div className="container mx-auto px-6">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'dashboard'
                  ? 'border-ey-yellow text-ey-yellow'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Vehicle Dashboard
            </button>
            <button
              onClick={() => setActiveTab('workflow')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'workflow'
                  ? 'border-ey-yellow text-ey-yellow'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Workflow Visualization
            </button>
            <button
              onClick={() => setActiveTab('stats')}
              className={`py-4 px-2 border-b-2 transition-colors ${
                activeTab === 'stats'
                  ? 'border-ey-yellow text-ey-yellow'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Analytics & Insights
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {activeTab === 'dashboard' && <VehicleDashboard />}
        {activeTab === 'workflow' && <WorkflowVisualization />}
        {activeTab === 'stats' && <StatsOverview />}
      </div>
    </main>
  )
}

