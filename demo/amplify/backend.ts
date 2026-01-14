import { defineBackend } from '@aws-amplify/backend'
import { Stack } from 'aws-cdk-lib'
import {
  Cors,
  LambdaIntegration,
  RestApi,
} from 'aws-cdk-lib/aws-apigateway'
import { Policy, PolicyStatement } from 'aws-cdk-lib/aws-iam'
import { auth } from './auth/resource'
import { villaApiFunction } from './functions/villa-api/resource'

const backend = defineBackend({
  auth,
  villaApiFunction,
})

// Create REST API stack
const apiStack = backend.createStack('villa-api-stack')

// Create REST API
const villaApi = new RestApi(apiStack, 'VillaRestApi', {
  restApiName: 'villa-sdk-api',
  deploy: true,
  deployOptions: {
    stageName: 'prod',
  },
  defaultCorsPreflightOptions: {
    allowOrigins: Cors.ALL_ORIGINS,
    allowMethods: Cors.ALL_METHODS,
    allowHeaders: ['Content-Type', 'Authorization', 'X-Api-Key'],
  },
})

// Lambda integration
const lambdaIntegration = new LambdaIntegration(
  backend.villaApiFunction.resources.lambda
)

// API Routes
const apiRoot = villaApi.root.addResource('api')

// Products endpoint
const productsPath = apiRoot.addResource('products')
productsPath.addMethod('GET', lambdaIntegration)

// Inventory endpoint
const inventoryPath = apiRoot.addResource('inventory')
inventoryPath.addMethod('GET', lambdaIntegration)

// Health check endpoint
const healthPath = apiRoot.addResource('health')
healthPath.addMethod('GET', lambdaIntegration)

// IAM policy for API access
const apiPolicy = new Policy(apiStack, 'VillaApiPolicy', {
  statements: [
    new PolicyStatement({
      actions: ['execute-api:Invoke'],
      resources: [
        `${villaApi.arnForExecuteApi('GET', '/api/products', 'prod')}`,
        `${villaApi.arnForExecuteApi('GET', '/api/inventory', 'prod')}`,
        `${villaApi.arnForExecuteApi('GET', '/api/health', 'prod')}`,
      ],
    }),
  ],
})

// Attach policy to authenticated users
backend.auth.resources.authenticatedUserIamRole.attachInlinePolicy(apiPolicy)

// Add API endpoint to outputs
backend.addOutput({
  custom: {
    VillaApi: {
      endpoint: villaApi.url,
      region: Stack.of(villaApi).region,
      apiName: villaApi.restApiName,
    },
  },
})
