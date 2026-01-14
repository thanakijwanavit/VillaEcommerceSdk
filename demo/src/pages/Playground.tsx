import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Play, 
  Terminal,
  Copy,
  Check,
  Code2,
  Loader2
} from 'lucide-react'

const examples = [
  {
    id: 'products',
    name: 'Get Products',
    code: `from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-cache")
products = client.get_product_list(branch=1000)
print(products.head(10))`,
  },
  {
    id: 'inventory',
    name: 'Get Inventory',
    code: `from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-cache")
inventory = client.get_inventory(branch=1000)
print(inventory[inventory['quantity'] < 50])`,
  },
  {
    id: 'merged',
    name: 'Products with Inventory',
    code: `from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-cache")
merged = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "Beverages"}
)
print(merged)`,
  },
  {
    id: 'analysis',
    name: 'Data Analysis',
    code: `from villa_ecommerce_sdk import VillaClient
import pandas as pd

client = VillaClient(s3_bucket="villa-cache")
df = client.get_products_with_inventory(branch=1000)

# Group by category
summary = df.groupby('category').agg({
    'price': 'mean',
    'quantity': 'sum'
}).round(2)

print(summary)`,
  },
]

// Mock output results
const mockOutputs: Record<string, string> = {
  products: `        sku           name     category  price  unit
0   TEA-001  Organic Green Tea  Beverages     89   box
1   COF-002  Premium Coffee     Beverages    245    kg
2   DAI-003  Fresh Milk 1L         Dairy     52  bottle
3   BAK-004  Whole Grain Bread     Bakery     45  loaf
4   DAI-005  Organic Eggs (12pk)    Dairy    125  pack
5   GRA-006  Thai Jasmine Rice     Grains     85    kg
6   BEV-007  Coconut Water       Beverages     35   can
7   SEA-008  Fresh Salmon Fillet  Seafood    580    kg
8   PRO-009  Avocado              Produce     75 piece
9   DAI-010  Greek Yogurt           Dairy     68   tub`,
  inventory: `        sku           name  quantity  min_stock   status
2   COF-002  Premium Coffee        25         30      low
4   BAK-004  Whole Grain Bread      5         20 critical
7   BEV-007  Coconut Water         45         50      low
8   SEA-008  Fresh Salmon           8         15 critical`,
  merged: `        sku           name     category  price  quantity   status
0   TEA-001  Organic Green Tea  Beverages     89       150       ok
1   COF-002  Premium Coffee     Beverages    245        85       ok
6   BEV-007  Coconut Water      Beverages     35       450       ok
11  BEV-012  Sparkling Water    Beverages     28       600       ok`,
  analysis: `category      price  quantity
Bakery        45.00        45
Beverages     99.25      1285
Dairy         81.67       615
Grains        85.00       500
Produce       75.00       180
Seafood      580.00        25
Spreads      195.00        42`,
}

export default function Playground() {
  const [selectedExample, setSelectedExample] = useState(examples[0])
  const [code, setCode] = useState(examples[0].code)
  const [output, setOutput] = useState('')
  const [running, setRunning] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleRun = () => {
    setRunning(true)
    setOutput('')
    
    // Simulate API call delay
    setTimeout(() => {
      setOutput(mockOutputs[selectedExample.id] || 'No output')
      setRunning(false)
    }, 1500)
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExampleChange = (example: typeof examples[0]) => {
    setSelectedExample(example)
    setCode(example.code)
    setOutput('')
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display text-3xl font-bold text-white mb-2">API Playground</h1>
          <p className="text-midnight-400">Try out the Villa SDK with interactive examples</p>
        </div>

        {/* Example Selector */}
        <div className="flex flex-wrap gap-2 mb-6">
          {examples.map((example) => (
            <button
              key={example.id}
              onClick={() => handleExampleChange(example)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all
                        ${selectedExample.id === example.id 
                          ? 'bg-villa-500/20 text-villa-400 border border-villa-500/30' 
                          : 'glass text-midnight-300 hover:text-white hover:bg-white/5'}`}
            >
              {example.name}
            </button>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Code Editor */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-2xl overflow-hidden"
          >
            <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-400/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-400/80" />
                  <div className="w-3 h-3 rounded-full bg-green-400/80" />
                </div>
                <span className="text-xs text-midnight-400 font-mono flex items-center gap-1.5">
                  <Code2 size={12} />
                  playground.py
                </span>
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                  title="Copy code"
                >
                  {copied ? (
                    <Check size={16} className="text-green-400" />
                  ) : (
                    <Copy size={16} className="text-midnight-400" />
                  )}
                </button>
                <button
                  onClick={handleRun}
                  disabled={running}
                  className="flex items-center gap-2 px-3 py-1.5 bg-villa-500/20 text-villa-400 
                           rounded-lg hover:bg-villa-500/30 transition-all disabled:opacity-50"
                >
                  {running ? (
                    <Loader2 size={16} className="animate-spin" />
                  ) : (
                    <Play size={16} />
                  )}
                  Run
                </button>
              </div>
            </div>
            
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-[400px] p-4 bg-transparent text-midnight-200 font-mono text-sm
                       resize-none focus:outline-none"
              spellCheck={false}
            />
          </motion.div>

          {/* Output */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-2xl overflow-hidden"
          >
            <div className="flex items-center gap-3 px-4 py-3 bg-white/5 border-b border-white/5">
              <Terminal size={16} className="text-midnight-400" />
              <span className="text-xs text-midnight-400 font-mono">Output</span>
            </div>
            
            <div className="h-[400px] p-4 overflow-auto">
              {running ? (
                <div className="flex items-center gap-3 text-midnight-400">
                  <Loader2 size={16} className="animate-spin" />
                  <span className="text-sm">Running...</span>
                </div>
              ) : output ? (
                <pre className="text-sm font-mono text-green-400 whitespace-pre-wrap">{output}</pre>
              ) : (
                <div className="text-midnight-500 text-sm">
                  Click "Run" to execute the code and see the output here.
                </div>
              )}
            </div>
          </motion.div>
        </div>

        {/* Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-8 glass rounded-2xl p-6"
        >
          <h2 className="text-lg font-semibold text-white mb-4">💡 Tips</h2>
          <ul className="space-y-2 text-sm text-midnight-300">
            <li className="flex items-start gap-2">
              <span className="text-villa-400">•</span>
              <span>This is a simulated playground. In production, the SDK connects to real Villa Market APIs.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-villa-400">•</span>
              <span>Data is cached in S3 to reduce API calls and improve performance.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-villa-400">•</span>
              <span>Use <code className="px-1.5 py-0.5 bg-midnight-800 rounded text-villa-400">force_refresh=True</code> to bypass the cache.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-villa-400">•</span>
              <span>All responses are pandas DataFrames - perfect for data analysis and visualization.</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  )
}
