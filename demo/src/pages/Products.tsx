import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  Filter, 
  RefreshCw, 
  Package,
  ChevronDown,
  Grid3X3,
  List,
  Tag
} from 'lucide-react'

interface Product {
  id: string
  name: string
  sku: string
  category: string
  price: number
  unit: string
  inStock: boolean
  quantity: number
  image?: string
}

// Mock data - will be replaced with actual API calls
const mockProducts: Product[] = [
  { id: '1', name: 'Organic Green Tea', sku: 'TEA-001', category: 'Beverages', price: 89, unit: 'box', inStock: true, quantity: 150 },
  { id: '2', name: 'Premium Coffee Beans', sku: 'COF-002', category: 'Beverages', price: 245, unit: 'kg', inStock: true, quantity: 85 },
  { id: '3', name: 'Fresh Milk 1L', sku: 'DAI-003', category: 'Dairy', price: 52, unit: 'bottle', inStock: true, quantity: 320 },
  { id: '4', name: 'Whole Grain Bread', sku: 'BAK-004', category: 'Bakery', price: 45, unit: 'loaf', inStock: false, quantity: 0 },
  { id: '5', name: 'Organic Eggs (12pk)', sku: 'DAI-005', category: 'Dairy', price: 125, unit: 'pack', inStock: true, quantity: 200 },
  { id: '6', name: 'Thai Jasmine Rice', sku: 'GRA-006', category: 'Grains', price: 85, unit: 'kg', inStock: true, quantity: 500 },
  { id: '7', name: 'Coconut Water', sku: 'BEV-007', category: 'Beverages', price: 35, unit: 'can', inStock: true, quantity: 450 },
  { id: '8', name: 'Fresh Salmon Fillet', sku: 'SEA-008', category: 'Seafood', price: 580, unit: 'kg', inStock: true, quantity: 25 },
  { id: '9', name: 'Avocado', sku: 'PRO-009', category: 'Produce', price: 75, unit: 'piece', inStock: true, quantity: 180 },
  { id: '10', name: 'Greek Yogurt', sku: 'DAI-010', category: 'Dairy', price: 68, unit: 'tub', inStock: true, quantity: 95 },
  { id: '11', name: 'Almond Butter', sku: 'SPR-011', category: 'Spreads', price: 195, unit: 'jar', inStock: true, quantity: 42 },
  { id: '12', name: 'Sparkling Water', sku: 'BEV-012', category: 'Beverages', price: 28, unit: 'bottle', inStock: true, quantity: 600 },
]

const categories = ['All', 'Beverages', 'Dairy', 'Bakery', 'Grains', 'Seafood', 'Produce', 'Spreads']

export default function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    // Simulate API call
    const timer = setTimeout(() => {
      setProducts(mockProducts)
      setLoading(false)
    }, 800)
    return () => clearTimeout(timer)
  }, [])

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.sku.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === 'All' || product.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const handleRefresh = () => {
    setLoading(true)
    setTimeout(() => {
      setProducts(mockProducts)
      setLoading(false)
    }, 800)
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display text-3xl font-bold text-white mb-2">Products</h1>
          <p className="text-midnight-400">Browse and search the product catalog from Villa Market APIs</p>
        </div>

        {/* Controls */}
        <div className="glass rounded-2xl p-4 mb-6">
          <div className="flex flex-wrap items-center gap-4">
            {/* Search */}
            <div className="flex-1 min-w-[280px] relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-midnight-400" size={20} />
              <input
                type="text"
                placeholder="Search products by name or SKU..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl
                         text-white placeholder:text-midnight-500 focus:border-villa-500/50
                         focus:bg-white/10 transition-all"
              />
            </div>

            {/* Category Filter */}
            <div className="relative">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center gap-2 px-4 py-3 glass rounded-xl hover:bg-white/10 transition-all"
              >
                <Filter size={18} className="text-midnight-400" />
                <span className="text-white">{selectedCategory}</span>
                <ChevronDown size={16} className={`text-midnight-400 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
              </button>
              
              {showFilters && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute top-full left-0 mt-2 w-48 glass-dark rounded-xl overflow-hidden z-20"
                >
                  {categories.map(category => (
                    <button
                      key={category}
                      onClick={() => {
                        setSelectedCategory(category)
                        setShowFilters(false)
                      }}
                      className={`w-full px-4 py-2 text-left text-sm hover:bg-white/10 transition-colors
                                ${selectedCategory === category ? 'text-villa-400 bg-villa-500/10' : 'text-midnight-200'}`}
                    >
                      {category}
                    </button>
                  ))}
                </motion.div>
              )}
            </div>

            {/* View Toggle */}
            <div className="flex items-center gap-1 p-1 glass rounded-xl">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-villa-500/20 text-villa-400' : 'text-midnight-400 hover:text-white'}`}
              >
                <Grid3X3 size={18} />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-lg transition-all ${viewMode === 'list' ? 'bg-villa-500/20 text-villa-400' : 'text-midnight-400 hover:text-white'}`}
              >
                <List size={18} />
              </button>
            </div>

            {/* Refresh */}
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-3 bg-villa-500/20 text-villa-400 rounded-xl
                       hover:bg-villa-500/30 transition-all disabled:opacity-50"
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              <span className="hidden sm:inline">Refresh</span>
            </button>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="flex items-center gap-6 mb-6 text-sm">
          <span className="text-midnight-400">
            Showing <span className="text-white font-medium">{filteredProducts.length}</span> of {products.length} products
          </span>
          {selectedCategory !== 'All' && (
            <span className="inline-flex items-center gap-1 px-3 py-1 bg-villa-500/20 text-villa-400 rounded-full">
              <Tag size={12} />
              {selectedCategory}
              <button 
                onClick={() => setSelectedCategory('All')}
                className="ml-1 hover:text-white"
              >
                ×
              </button>
            </span>
          )}
        </div>

        {/* Products Grid/List */}
        {loading ? (
          <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4' : 'space-y-3'}>
            {[...Array(8)].map((_, i) => (
              <div key={i} className="glass rounded-2xl p-6">
                <div className="skeleton h-32 rounded-xl mb-4" />
                <div className="skeleton h-4 w-3/4 rounded mb-2" />
                <div className="skeleton h-3 w-1/2 rounded" />
              </div>
            ))}
          </div>
        ) : viewMode === 'grid' ? (
          <motion.div 
            className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
            initial="hidden"
            animate="visible"
            variants={{
              visible: { transition: { staggerChildren: 0.05 } }
            }}
          >
            {filteredProducts.map((product) => (
              <motion.div
                key={product.id}
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0 }
                }}
                className="glass rounded-2xl p-5 hover:bg-white/5 transition-all group cursor-pointer"
              >
                <div className="aspect-square rounded-xl bg-gradient-to-br from-midnight-700 to-midnight-800 
                              flex items-center justify-center mb-4 group-hover:from-midnight-600 
                              group-hover:to-midnight-700 transition-all">
                  <Package className="text-midnight-500 group-hover:text-villa-500/50 transition-colors" size={48} />
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-semibold text-white leading-tight">{product.name}</h3>
                    <span className={`shrink-0 w-2 h-2 rounded-full mt-2 ${product.inStock ? 'bg-green-400' : 'bg-red-400'}`} />
                  </div>
                  
                  <p className="text-xs font-mono text-midnight-500">{product.sku}</p>
                  
                  <div className="flex items-center justify-between pt-2">
                    <span className="text-villa-400 font-semibold">฿{product.price}/{product.unit}</span>
                    <span className="text-xs text-midnight-500">{product.quantity} units</span>
                  </div>
                  
                  <span className="inline-block text-xs px-2 py-1 bg-midnight-800 text-midnight-300 rounded-lg">
                    {product.category}
                  </span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <motion.div 
            className="space-y-3"
            initial="hidden"
            animate="visible"
            variants={{
              visible: { transition: { staggerChildren: 0.03 } }
            }}
          >
            {filteredProducts.map((product) => (
              <motion.div
                key={product.id}
                variants={{
                  hidden: { opacity: 0, x: -20 },
                  visible: { opacity: 1, x: 0 }
                }}
                className="glass rounded-xl p-4 hover:bg-white/5 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-xl bg-midnight-800 flex items-center justify-center shrink-0">
                    <Package className="text-midnight-500" size={24} />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-white truncate">{product.name}</h3>
                      <span className={`shrink-0 w-2 h-2 rounded-full ${product.inStock ? 'bg-green-400' : 'bg-red-400'}`} />
                    </div>
                    <div className="flex items-center gap-3 text-sm text-midnight-400">
                      <span className="font-mono">{product.sku}</span>
                      <span className="px-2 py-0.5 bg-midnight-800 rounded text-xs">{product.category}</span>
                    </div>
                  </div>
                  
                  <div className="text-right shrink-0">
                    <div className="text-villa-400 font-semibold">฿{product.price}/{product.unit}</div>
                    <div className="text-xs text-midnight-500">{product.quantity} units</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {filteredProducts.length === 0 && !loading && (
          <div className="text-center py-16">
            <Package className="mx-auto text-midnight-600 mb-4" size={48} />
            <p className="text-midnight-400">No products found matching your criteria</p>
          </div>
        )}
      </div>
    </div>
  )
}
