# Villa Ecommerce SDK Demo

An interactive React demo application showcasing the Villa Ecommerce SDK capabilities. Built with React, TypeScript, and AWS Amplify Gen 2.

## 🚀 Features

- **Products Browser**: Search and filter products from the Villa catalog
- **Inventory Dashboard**: Real-time stock levels across branches
- **Documentation**: Interactive SDK documentation with code examples
- **API Playground**: Try SDK commands with live output simulation

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS with custom design system
- **Animation**: Framer Motion
- **Icons**: Lucide React
- **Backend**: AWS Amplify Gen 2
  - Lambda functions
  - API Gateway
  - Cognito Authentication

## 📦 Installation

```bash
# Navigate to demo directory
cd demo

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Development

### Local Development

```bash
npm run dev
```

Opens at `http://localhost:5173`

### Amplify Sandbox

Deploy a personal sandbox environment:

```bash
npm run sandbox
```

This creates isolated AWS resources for testing.

### Build for Production

```bash
npm run build
npm run preview
```

## 🏗️ Project Structure

```
demo/
├── amplify/                    # Amplify Gen 2 backend
│   ├── auth/
│   │   └── resource.ts        # Auth configuration
│   ├── functions/
│   │   └── villa-api/
│   │       ├── handler.ts     # API Lambda handler
│   │       └── resource.ts    # Function definition
│   └── backend.ts             # Backend orchestration
├── src/
│   ├── components/
│   │   └── Layout.tsx         # App layout with nav
│   ├── pages/
│   │   ├── Home.tsx           # Landing page
│   │   ├── Products.tsx       # Product catalog
│   │   ├── Inventory.tsx      # Stock dashboard
│   │   ├── Documentation.tsx  # SDK docs
│   │   └── Playground.tsx     # API playground
│   ├── App.tsx                # Router setup
│   ├── main.tsx               # Entry point
│   └── index.css              # Global styles
├── public/
│   └── villa.svg              # App icon
└── package.json
```

## 🎨 Design System

### Colors

| Name | Hex | Usage |
|------|-----|-------|
| Villa Primary | `#e87422` | Accents, CTAs, highlights |
| Midnight | `#0f1422` | Background |
| Midnight Light | `#cbd7ec` | Text |

### Typography

- **Display**: Clash Display / Outfit (headings)
- **Body**: Outfit (text)
- **Mono**: JetBrains Mono (code)

### Components

- Glass morphism containers with `glass` class
- Rounded corners (`rounded-xl`, `rounded-2xl`)
- Subtle orange glow effects with `glow` class

## 🔗 SDK Integration

This demo showcases the [Villa Ecommerce SDK](../python/README.md). Key integrations:

- Product listing from `client.get_product_list()`
- Inventory data from `client.get_inventory()`
- Merged data from `client.get_products_with_inventory()`

## 📚 Related Documentation

- [Python SDK README](../python/README.md)
- [API Documentation](../docs/api/python.md)
- [AWS Setup Guide](../docs/aws-setup/README.md)

## 🚢 Deployment

### AWS Amplify Hosting

1. Connect your repo to AWS Amplify Console
2. Amplify auto-detects the `demo/` folder
3. Push to `main` triggers automatic deployment

### Manual Deployment

```bash
npm run build
# Deploy dist/ to your hosting provider
```

## 📄 License

MIT License - Part of the Villa Ecommerce SDK project.
