import { Outlet, NavLink, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Home, 
  Package, 
  BarChart3, 
  BookOpen, 
  Code2,
  Github,
  ExternalLink
} from 'lucide-react'

const navItems = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/products', label: 'Products', icon: Package },
  { path: '/inventory', label: 'Inventory', icon: BarChart3 },
  { path: '/docs', label: 'Docs', icon: BookOpen },
  { path: '/playground', label: 'Playground', icon: Code2 },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 glass-dark flex flex-col z-50">
        {/* Logo */}
        <div className="p-6 border-b border-white/5">
          <NavLink to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-villa-500 to-villa-600 flex items-center justify-center shadow-lg glow group-hover:glow-strong transition-all">
              <span className="text-white font-bold text-lg">V</span>
            </div>
            <div>
              <h1 className="font-display font-bold text-white text-lg leading-none">Villa SDK</h1>
              <span className="text-xs text-villa-400 font-medium">Demo</span>
            </div>
          </NavLink>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={`
                  relative flex items-center gap-3 px-4 py-3 rounded-xl font-medium
                  transition-all duration-200
                  ${isActive 
                    ? 'text-white' 
                    : 'text-midnight-300 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute inset-0 bg-gradient-to-r from-villa-500/20 to-villa-600/10 rounded-xl border border-villa-500/30"
                    initial={false}
                    transition={{ type: 'spring', stiffness: 500, damping: 35 }}
                  />
                )}
                <Icon size={20} className="relative z-10" />
                <span className="relative z-10">{item.label}</span>
              </NavLink>
            )
          })}
        </nav>

        {/* Footer Links */}
        <div className="p-4 border-t border-white/5">
          <a 
            href="https://github.com/your-org/VillaEcommerceSdk"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 text-sm text-midnight-400 hover:text-white transition-colors"
          >
            <Github size={16} />
            <span>View on GitHub</span>
            <ExternalLink size={12} className="ml-auto opacity-50" />
          </a>
          <a 
            href="https://pypi.org/project/villa-ecommerce-sdk/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 text-sm text-midnight-400 hover:text-white transition-colors"
          >
            <Package size={16} />
            <span>PyPI Package</span>
            <ExternalLink size={12} className="ml-auto opacity-50" />
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            className="min-h-screen"
          >
            <Outlet />
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  )
}
