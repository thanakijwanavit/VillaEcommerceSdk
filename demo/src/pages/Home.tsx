import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Package, 
  BarChart3, 
  Zap, 
  Shield, 
  Database,
  ArrowRight,
  Terminal,
  Sparkles
} from 'lucide-react'

const features = [
  {
    icon: Package,
    title: 'Product Catalog',
    description: 'Fetch and display product listings with real-time data from Villa Market APIs.',
  },
  {
    icon: BarChart3,
    title: 'Inventory Tracking',
    description: 'Monitor stock levels across branches with automatic sync and caching.',
  },
  {
    icon: Database,
    title: 'S3 Caching',
    description: 'Intelligent caching layer using AWS S3 for fast, reliable data access.',
  },
  {
    icon: Zap,
    title: 'Real-time Sync',
    description: 'Keep your data fresh with configurable cache TTL and background refresh.',
  },
  {
    icon: Shield,
    title: 'Type-Safe',
    description: 'Full TypeScript support with comprehensive type definitions.',
  },
  {
    icon: Sparkles,
    title: 'Pandas Ready',
    description: 'Data returned as DataFrames for easy analysis and manipulation.',
  },
]

const codeExample = `from villa_ecommerce_sdk import VillaClient

# Initialize the client
client = VillaClient(s3_bucket="my-cache-bucket")

# Fetch products with inventory data
products = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "beverages"}
)

# Access as pandas DataFrame
print(products.head())`

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative px-8 py-20 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-radial from-villa-500/10 via-transparent to-transparent" />
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-villa-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-midnight-500/20 rounded-full blur-3xl" />
        
        <div className="relative max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              <span className="text-sm text-midnight-200">SDK v0.3.0 Available</span>
            </div>
            
            <h1 className="font-display text-5xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="text-white">Villa Ecommerce</span>
              <br />
              <span className="gradient-text">SDK Demo</span>
            </h1>
            
            <p className="text-xl text-midnight-300 max-w-2xl mx-auto mb-10">
              Explore the full capabilities of the Villa SDK. Browse products, 
              check inventory, and interact with real API data in this live demo.
            </p>
            
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Link
                to="/products"
                className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-villa-500 to-villa-600 
                         text-white font-semibold rounded-xl hover:from-villa-400 hover:to-villa-500 
                         transition-all glow hover:glow-strong"
              >
                <Package size={20} />
                Explore Products
                <ArrowRight size={18} />
              </Link>
              
              <Link
                to="/playground"
                className="inline-flex items-center gap-2 px-6 py-3 glass text-white font-semibold 
                         rounded-xl hover:bg-white/10 transition-all"
              >
                <Terminal size={20} />
                API Playground
              </Link>
            </div>
          </motion.div>

          {/* Code Preview */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="glass rounded-2xl overflow-hidden glow"
          >
            <div className="flex items-center gap-2 px-4 py-3 bg-white/5 border-b border-white/5">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-400/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-400/80" />
                <div className="w-3 h-3 rounded-full bg-green-400/80" />
              </div>
              <span className="text-xs text-midnight-400 ml-4 font-mono">example.py</span>
            </div>
            <pre className="p-6 overflow-x-auto">
              <code className="text-sm font-mono text-midnight-200">
                {codeExample}
              </code>
            </pre>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-8 py-20">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-4">
              Everything You Need
            </h2>
            <p className="text-midnight-300 max-w-xl mx-auto">
              The Villa SDK provides a complete toolkit for integrating with Villa Market APIs.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="glass rounded-2xl p-6 hover:bg-white/5 transition-all group"
                >
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-villa-500/20 to-villa-600/10 
                                flex items-center justify-center mb-4 group-hover:from-villa-500/30 
                                group-hover:to-villa-600/20 transition-all">
                    <Icon className="text-villa-400" size={24} />
                  </div>
                  <h3 className="font-semibold text-white text-lg mb-2">{feature.title}</h3>
                  <p className="text-midnight-400 text-sm leading-relaxed">{feature.description}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Quick Install */}
      <section className="px-8 py-20">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass rounded-2xl p-8 text-center"
          >
            <h2 className="font-display text-2xl font-bold text-white mb-4">
              Get Started in Seconds
            </h2>
            <p className="text-midnight-300 mb-6">
              Install the Python SDK and start fetching data immediately.
            </p>
            <div className="inline-flex items-center gap-3 px-6 py-3 bg-midnight-950 rounded-xl font-mono text-sm">
              <span className="text-villa-400">$</span>
              <span className="text-white">pip install villa-ecommerce-sdk</span>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
