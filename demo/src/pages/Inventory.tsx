import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle,
  Package,
  RefreshCw,
  MapPin,
  Clock
} from 'lucide-react'

interface InventoryItem {
  id: string
  productName: string
  sku: string
  branch: number
  branchName: string
  quantity: number
  minStock: number
  lastUpdated: string
  status: 'ok' | 'low' | 'critical'
}

// Mock data
const mockInventory: InventoryItem[] = [
  { id: '1', productName: 'Organic Green Tea', sku: 'TEA-001', branch: 1000, branchName: 'Siam Paragon', quantity: 150, minStock: 50, lastUpdated: '2 mins ago', status: 'ok' },
  { id: '2', productName: 'Premium Coffee Beans', sku: 'COF-002', branch: 1000, branchName: 'Siam Paragon', quantity: 25, minStock: 30, lastUpdated: '5 mins ago', status: 'low' },
  { id: '3', productName: 'Fresh Milk 1L', sku: 'DAI-003', branch: 1001, branchName: 'EmQuartier', quantity: 320, minStock: 100, lastUpdated: '1 min ago', status: 'ok' },
  { id: '4', productName: 'Whole Grain Bread', sku: 'BAK-004', branch: 1001, branchName: 'EmQuartier', quantity: 5, minStock: 20, lastUpdated: '10 mins ago', status: 'critical' },
  { id: '5', productName: 'Organic Eggs (12pk)', sku: 'DAI-005', branch: 1002, branchName: 'CentralWorld', quantity: 200, minStock: 50, lastUpdated: '3 mins ago', status: 'ok' },
  { id: '6', productName: 'Thai Jasmine Rice', sku: 'GRA-006', branch: 1000, branchName: 'Siam Paragon', quantity: 500, minStock: 100, lastUpdated: '8 mins ago', status: 'ok' },
  { id: '7', productName: 'Coconut Water', sku: 'BEV-007', branch: 1002, branchName: 'CentralWorld', quantity: 45, minStock: 50, lastUpdated: '4 mins ago', status: 'low' },
  { id: '8', productName: 'Fresh Salmon Fillet', sku: 'SEA-008', branch: 1001, branchName: 'EmQuartier', quantity: 8, minStock: 15, lastUpdated: '1 min ago', status: 'critical' },
]

const branches = [
  { id: 1000, name: 'Siam Paragon' },
  { id: 1001, name: 'EmQuartier' },
  { id: 1002, name: 'CentralWorld' },
]

export default function Inventory() {
  const [inventory, setInventory] = useState<InventoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedBranch, setSelectedBranch] = useState<number | null>(null)

  useEffect(() => {
    const timer = setTimeout(() => {
      setInventory(mockInventory)
      setLoading(false)
    }, 800)
    return () => clearTimeout(timer)
  }, [])

  const filteredInventory = selectedBranch 
    ? inventory.filter(item => item.branch === selectedBranch)
    : inventory

  const stats = {
    total: inventory.length,
    ok: inventory.filter(i => i.status === 'ok').length,
    low: inventory.filter(i => i.status === 'low').length,
    critical: inventory.filter(i => i.status === 'critical').length,
  }

  const handleRefresh = () => {
    setLoading(true)
    setTimeout(() => {
      setInventory(mockInventory)
      setLoading(false)
    }, 800)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ok': return 'text-green-400 bg-green-400/10'
      case 'low': return 'text-yellow-400 bg-yellow-400/10'
      case 'critical': return 'text-red-400 bg-red-400/10'
      default: return 'text-midnight-400 bg-midnight-800'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ok': return TrendingUp
      case 'low': return TrendingDown
      case 'critical': return AlertTriangle
      default: return Package
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-wrap items-start justify-between gap-4 mb-8">
          <div>
            <h1 className="font-display text-3xl font-bold text-white mb-2">Inventory</h1>
            <p className="text-midnight-400">Real-time stock levels across all branches</p>
          </div>
          
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-villa-500/20 text-villa-400 rounded-xl
                     hover:bg-villa-500/30 transition-all disabled:opacity-50"
          >
            <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
            Sync Now
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <BarChart3 className="text-villa-400" size={24} />
              <span className="text-xs text-midnight-500">Total Items</span>
            </div>
            <div className="text-3xl font-bold text-white">{stats.total}</div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass rounded-2xl p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <TrendingUp className="text-green-400" size={24} />
              <span className="text-xs text-midnight-500">In Stock</span>
            </div>
            <div className="text-3xl font-bold text-green-400">{stats.ok}</div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass rounded-2xl p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <TrendingDown className="text-yellow-400" size={24} />
              <span className="text-xs text-midnight-500">Low Stock</span>
            </div>
            <div className="text-3xl font-bold text-yellow-400">{stats.low}</div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass rounded-2xl p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <AlertTriangle className="text-red-400" size={24} />
              <span className="text-xs text-midnight-500">Critical</span>
            </div>
            <div className="text-3xl font-bold text-red-400">{stats.critical}</div>
          </motion.div>
        </div>

        {/* Branch Filter */}
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <span className="text-sm text-midnight-400">Filter by branch:</span>
          <button
            onClick={() => setSelectedBranch(null)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all
                      ${selectedBranch === null 
                        ? 'bg-villa-500/20 text-villa-400 border border-villa-500/30' 
                        : 'glass text-midnight-300 hover:text-white hover:bg-white/5'}`}
          >
            All Branches
          </button>
          {branches.map(branch => (
            <button
              key={branch.id}
              onClick={() => setSelectedBranch(branch.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all
                        ${selectedBranch === branch.id 
                          ? 'bg-villa-500/20 text-villa-400 border border-villa-500/30' 
                          : 'glass text-midnight-300 hover:text-white hover:bg-white/5'}`}
            >
              <MapPin size={14} />
              {branch.name}
            </button>
          ))}
        </div>

        {/* Inventory Table */}
        <div className="glass rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/5">
                  <th className="text-left px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Product</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Branch</th>
                  <th className="text-right px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Quantity</th>
                  <th className="text-right px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Min Stock</th>
                  <th className="text-center px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Status</th>
                  <th className="text-right px-6 py-4 text-xs font-semibold text-midnight-400 uppercase tracking-wider">Updated</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  [...Array(5)].map((_, i) => (
                    <tr key={i} className="border-b border-white/5">
                      <td className="px-6 py-4"><div className="skeleton h-4 w-40 rounded" /></td>
                      <td className="px-6 py-4"><div className="skeleton h-4 w-24 rounded" /></td>
                      <td className="px-6 py-4"><div className="skeleton h-4 w-12 rounded ml-auto" /></td>
                      <td className="px-6 py-4"><div className="skeleton h-4 w-12 rounded ml-auto" /></td>
                      <td className="px-6 py-4"><div className="skeleton h-6 w-16 rounded mx-auto" /></td>
                      <td className="px-6 py-4"><div className="skeleton h-4 w-20 rounded ml-auto" /></td>
                    </tr>
                  ))
                ) : (
                  filteredInventory.map((item, index) => {
                    const StatusIcon = getStatusIcon(item.status)
                    return (
                      <motion.tr
                        key={item.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: index * 0.05 }}
                        className="border-b border-white/5 hover:bg-white/5 transition-colors"
                      >
                        <td className="px-6 py-4">
                          <div>
                            <div className="font-medium text-white">{item.productName}</div>
                            <div className="text-xs font-mono text-midnight-500">{item.sku}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2 text-midnight-300">
                            <MapPin size={14} className="text-midnight-500" />
                            {item.branchName}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <span className="font-mono text-white">{item.quantity}</span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <span className="font-mono text-midnight-500">{item.minStock}</span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex justify-center">
                            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}>
                              <StatusIcon size={12} />
                              {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex items-center justify-end gap-1.5 text-midnight-500 text-sm">
                            <Clock size={12} />
                            {item.lastUpdated}
                          </div>
                        </td>
                      </motion.tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {filteredInventory.length === 0 && !loading && (
          <div className="text-center py-16">
            <Package className="mx-auto text-midnight-600 mb-4" size={48} />
            <p className="text-midnight-400">No inventory data for selected branch</p>
          </div>
        )}
      </div>
    </div>
  )
}
