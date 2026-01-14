import type { APIGatewayProxyHandler, APIGatewayProxyResult } from 'aws-lambda'

// Mock data for demo purposes
// In production, this would call the actual Villa API via Python SDK layer
const mockProducts = [
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

const mockInventory = [
  { id: '1', productName: 'Organic Green Tea', sku: 'TEA-001', branch: 1000, branchName: 'Siam Paragon', quantity: 150, minStock: 50, lastUpdated: new Date().toISOString(), status: 'ok' },
  { id: '2', productName: 'Premium Coffee Beans', sku: 'COF-002', branch: 1000, branchName: 'Siam Paragon', quantity: 25, minStock: 30, lastUpdated: new Date().toISOString(), status: 'low' },
  { id: '3', productName: 'Fresh Milk 1L', sku: 'DAI-003', branch: 1001, branchName: 'EmQuartier', quantity: 320, minStock: 100, lastUpdated: new Date().toISOString(), status: 'ok' },
  { id: '4', productName: 'Whole Grain Bread', sku: 'BAK-004', branch: 1001, branchName: 'EmQuartier', quantity: 5, minStock: 20, lastUpdated: new Date().toISOString(), status: 'critical' },
  { id: '5', productName: 'Organic Eggs (12pk)', sku: 'DAI-005', branch: 1002, branchName: 'CentralWorld', quantity: 200, minStock: 50, lastUpdated: new Date().toISOString(), status: 'ok' },
  { id: '6', productName: 'Thai Jasmine Rice', sku: 'GRA-006', branch: 1000, branchName: 'Siam Paragon', quantity: 500, minStock: 100, lastUpdated: new Date().toISOString(), status: 'ok' },
  { id: '7', productName: 'Coconut Water', sku: 'BEV-007', branch: 1002, branchName: 'CentralWorld', quantity: 45, minStock: 50, lastUpdated: new Date().toISOString(), status: 'low' },
  { id: '8', productName: 'Fresh Salmon Fillet', sku: 'SEA-008', branch: 1001, branchName: 'EmQuartier', quantity: 8, minStock: 15, lastUpdated: new Date().toISOString(), status: 'critical' },
]

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Api-Key',
  'Access-Control-Allow-Methods': 'GET,OPTIONS',
  'Content-Type': 'application/json',
}

function response(statusCode: number, body: unknown): APIGatewayProxyResult {
  return {
    statusCode,
    headers: corsHeaders,
    body: JSON.stringify(body),
  }
}

export const handler: APIGatewayProxyHandler = async (event) => {
  const { path, httpMethod, queryStringParameters } = event

  console.log(`[Villa API] ${httpMethod} ${path}`, { queryStringParameters })

  // Health check
  if (path.endsWith('/health')) {
    return response(200, {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      environment: {
        baseUrl: process.env.VILLA_API_BASE_URL,
        cacheBucket: process.env.S3_CACHE_BUCKET,
      },
    })
  }

  // Products endpoint
  if (path.endsWith('/products')) {
    const category = queryStringParameters?.category
    const search = queryStringParameters?.search?.toLowerCase()

    let products = [...mockProducts]

    if (category && category !== 'All') {
      products = products.filter(p => p.category === category)
    }

    if (search) {
      products = products.filter(p =>
        p.name.toLowerCase().includes(search) ||
        p.sku.toLowerCase().includes(search)
      )
    }

    return response(200, {
      success: true,
      data: products,
      meta: {
        total: products.length,
        cached: true,
        cacheAge: '5m',
      },
    })
  }

  // Inventory endpoint
  if (path.endsWith('/inventory')) {
    const branch = queryStringParameters?.branch
      ? parseInt(queryStringParameters.branch)
      : null

    let inventory = [...mockInventory]

    if (branch) {
      inventory = inventory.filter(i => i.branch === branch)
    }

    return response(200, {
      success: true,
      data: inventory,
      meta: {
        total: inventory.length,
        cached: true,
        cacheAge: '2m',
      },
    })
  }

  // 404 for unknown routes
  return response(404, {
    success: false,
    error: 'Not Found',
    message: `Unknown endpoint: ${path}`,
  })
}
