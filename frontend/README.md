# AskAfrica Frontend

Next.js frontend for the AskAfrica AI Q&A application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Make sure the backend is running on `http://localhost:8000`

## Running the Frontend

```bash
npm run dev
```

The application will be available at:
- http://localhost:3000

## Features

- Modern, responsive UI with TailwindCSS
- Real-time AI Q&A interface
- Loading states and error handling
- Recent questions stored in localStorage
- Beautiful gradient design

## Development

- Built with Next.js 15 and TypeScript
- Styled with TailwindCSS
- Uses client-side state management
- Integrates with FastAPI backend

## API Integration

The frontend communicates with the backend at `http://localhost:8000/ask` endpoint.
