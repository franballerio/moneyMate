# MoneyMate Frontend

A modern React + TypeScript + TailwindCSS dashboard for personal finance management.

## Features

- 📊 **Dashboard** - Real-time spending metrics and budget overview
- 💳 **Transactions** - View, filter, and manage all expenses
- 💰 **Budgets** - Set and track category-based spending limits
- 📈 **Analytics** - Advanced spending insights and trends
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Beautiful, intuitive interface with TailwindCSS

## Tech Stack

- **React 18** with TypeScript
- **Vite** - Next generation frontend build tool
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - React charting library
- **Axios** - HTTP client
- **React Router** - Client-side routing

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file (copy from `.env.example`):
```bash
cp .env.example .env.local
```

3. Update `VITE_API_BASE_URL` in `.env.local` if your backend is running on a different port:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Create production build:
```bash
npm run build
```

### Preview

Preview production build locally:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout/           # Sidebar, Header, Layout wrapper
│   │   ├── Dashboard/        # Dashboard components
│   │   ├── Charts/           # Chart components (Trends, Categories)
│   │   └── Transactions/     # Transaction table
│   ├── pages/                # Page components (Dashboard, Transactions, etc.)
│   ├── services/
│   │   ├── apiClient.ts      # Axios instance with interceptors
│   │   └── api.ts            # API hooks and types
│   ├── App.tsx               # Main app with routing
│   ├── main.tsx              # Entry point
│   └── index.css             # TailwindCSS styles
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## API Integration

The frontend communicates with the FastAPI backend through REST endpoints.

### Environment Variables

- `VITE_API_BASE_URL` - API base URL (default: `http://localhost:8000/api/v1`)
- `VITE_ENVIRONMENT` - Environment (development/production)

### API Endpoints Used

- `GET /api/v1/expenses` - Fetch paginated expenses
- `GET /api/v1/metrics/summary` - Fetch metrics summary
- `GET /api/v1/metrics/categories` - Fetch category breakdown
- `GET /api/v1/metrics/trends` - Fetch spending trends
- `GET /api/v1/budgets` - Fetch user budgets

## Features In Progress

- User authentication (login/register)
- Create/edit/delete transactions
- Budget management UI
- Advanced analytics and reports
- Offline support with service workers
- Dark mode theme toggle

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT
