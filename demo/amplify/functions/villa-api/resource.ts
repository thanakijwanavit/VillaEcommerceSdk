import { defineFunction } from '@aws-amplify/backend'

export const villaApiFunction = defineFunction({
  name: 'villa-api-handler',
  entry: './handler.ts',
  timeoutSeconds: 30,
  memoryMB: 256,
  environment: {
    VILLA_API_BASE_URL: 'https://api.villa.kitchen',
    S3_CACHE_BUCKET: 'villa-ecommerce-sdk-cache',
    CACHE_TTL_SECONDS: '3600',
  },
  runtime: 20, // Node.js 20
})
