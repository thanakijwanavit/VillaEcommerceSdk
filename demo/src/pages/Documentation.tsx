import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Code2, 
  Terminal,
  FileCode,
  ExternalLink,
  Copy,
  Check
} from 'lucide-react'
import { useState } from 'react'

const sections = [
  {
    id: 'installation',
    title: 'Installation',
    content: `Install the Villa Ecommerce SDK using pip:

\`\`\`bash
pip install villa-ecommerce-sdk
\`\`\`

Make sure you have Python 3.8 or higher installed.`,
  },
  {
    id: 'quickstart',
    title: 'Quick Start',
    content: `Initialize the client and start fetching data:

\`\`\`python
from villa_ecommerce_sdk import VillaClient

# Initialize with your S3 cache bucket
client = VillaClient(s3_bucket="my-cache-bucket")

# Fetch product list
products = client.get_product_list(branch=1000)

# Fetch inventory data
inventory = client.get_inventory(branch=1000)

# Merge products with inventory
merged = client.get_products_with_inventory(branch=1000)
\`\`\``,
  },
  {
    id: 'authentication',
    title: 'Authentication',
    content: `The SDK uses AWS credentials for S3 access. Make sure your AWS credentials are configured:

\`\`\`bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=ap-southeast-1
\`\`\``,
  },
  {
    id: 'caching',
    title: 'S3 Caching',
    content: `The SDK automatically caches API responses to S3:

\`\`\`python
# Configure cache settings
client = VillaClient(
    s3_bucket="my-cache-bucket",
    cache_ttl=3600  # 1 hour TTL
)

# Force refresh (bypass cache)
products = client.get_product_list(
    branch=1000,
    force_refresh=True
)

# Check cache status
status = client.get_cache_status()
\`\`\``,
  },
  {
    id: 'dataframes',
    title: 'Working with DataFrames',
    content: `All data is returned as pandas DataFrames for easy manipulation:

\`\`\`python
import pandas as pd

# Get products
df = client.get_product_list(branch=1000)

# Filter by category
beverages = df[df['category'] == 'Beverages']

# Sort by price
sorted_df = df.sort_values('price', ascending=False)

# Group by category
grouped = df.groupby('category')['price'].mean()

# Export to CSV
df.to_csv('products.csv', index=False)
\`\`\``,
  },
]

function CodeBlock({ code }: { code: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative group">
      <pre className="bg-midnight-950 rounded-xl p-4 overflow-x-auto">
        <code className="text-sm font-mono text-midnight-200">{code}</code>
      </pre>
      <button
        onClick={handleCopy}
        className="absolute top-3 right-3 p-2 rounded-lg bg-white/5 opacity-0 group-hover:opacity-100
                 transition-opacity hover:bg-white/10"
      >
        {copied ? <Check size={16} className="text-green-400" /> : <Copy size={16} className="text-midnight-400" />}
      </button>
    </div>
  )
}

function renderContent(content: string) {
  const parts = content.split(/(```[\s\S]*?```)/g)
  
  return parts.map((part, index) => {
    if (part.startsWith('```')) {
      const match = part.match(/```(\w+)?\n([\s\S]*?)```/)
      if (match) {
        return <CodeBlock key={index} code={match[2].trim()} />
      }
    }
    
    return (
      <div key={index} className="text-midnight-300 leading-relaxed whitespace-pre-line">
        {part.split('\n').map((line, i) => {
          if (line.includes('`') && !line.includes('```')) {
            const formatted = line.split(/(`[^`]+`)/g).map((segment, j) => {
              if (segment.startsWith('`') && segment.endsWith('`')) {
                return (
                  <code key={j} className="px-1.5 py-0.5 bg-midnight-800 rounded text-villa-400 text-sm font-mono">
                    {segment.slice(1, -1)}
                  </code>
                )
              }
              return segment
            })
            return <span key={i}>{formatted}</span>
          }
          return <span key={i}>{line}</span>
        })}
      </div>
    )
  })
}

export default function Documentation() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="font-display text-3xl font-bold text-white mb-2">Documentation</h1>
          <p className="text-midnight-400">Learn how to use the Villa Ecommerce SDK</p>
        </div>

        {/* Quick Links */}
        <div className="glass rounded-2xl p-6 mb-8">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <BookOpen size={20} className="text-villa-400" />
            Quick Links
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <a 
              href="https://pypi.org/project/villa-ecommerce-sdk/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group"
            >
              <FileCode className="text-villa-400" size={20} />
              <span className="text-midnight-200 group-hover:text-white">PyPI Package</span>
              <ExternalLink size={14} className="ml-auto opacity-50" />
            </a>
            <a 
              href="https://github.com/your-org/VillaEcommerceSdk"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group"
            >
              <Code2 className="text-villa-400" size={20} />
              <span className="text-midnight-200 group-hover:text-white">GitHub Repo</span>
              <ExternalLink size={14} className="ml-auto opacity-50" />
            </a>
            <a 
              href="#"
              className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group"
            >
              <Terminal className="text-villa-400" size={20} />
              <span className="text-midnight-200 group-hover:text-white">API Reference</span>
              <ExternalLink size={14} className="ml-auto opacity-50" />
            </a>
          </div>
        </div>

        {/* Documentation Sections */}
        <div className="space-y-8">
          {sections.map((section, index) => (
            <motion.section
              key={section.id}
              id={section.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="glass rounded-2xl p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <span className="w-8 h-8 rounded-lg bg-villa-500/20 flex items-center justify-center text-villa-400 text-sm font-mono">
                  {index + 1}
                </span>
                {section.title}
              </h2>
              <div className="space-y-4">
                {renderContent(section.content)}
              </div>
            </motion.section>
          ))}
        </div>

        {/* Need Help */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-12 glass rounded-2xl p-8 text-center"
        >
          <h2 className="text-xl font-semibold text-white mb-2">Need Help?</h2>
          <p className="text-midnight-400 mb-4">
            Check out our GitHub repository for issues, discussions, and more examples.
          </p>
          <a
            href="https://github.com/your-org/VillaEcommerceSdk/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-villa-500/20 text-villa-400 
                     rounded-xl hover:bg-villa-500/30 transition-all"
          >
            Open an Issue
            <ExternalLink size={16} />
          </a>
        </motion.div>
      </div>
    </div>
  )
}
