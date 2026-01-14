import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Products from './pages/Products'
import Inventory from './pages/Inventory'
import Documentation from './pages/Documentation'
import Playground from './pages/Playground'

function App() {
  return (
    <BrowserRouter>
      <div className="noise-overlay" />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/docs" element={<Documentation />} />
          <Route path="/playground" element={<Playground />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
