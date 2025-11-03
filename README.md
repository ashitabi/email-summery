# CE Email Summarization Tool

AI-powered customer experience email thread analysis and summarization prototype with human-in-the-loop review workflow.

## 🚀 Quick Start

```bash
# Terminal 1: Start Backend
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser!

## Overview

This prototype demonstrates an end-to-end workflow for processing multi-threaded customer support emails:
1. Load and parse email threads (JSON format)
2. Generate AI summaries with key information extraction
3. Human review and editing interface
4. Approval workflow for CRM integration

## Tech Stack

### Frontend
- **React 18** with **TypeScript** for type safety
- **Vite** for fast development and optimized builds
- Vanilla CSS for styling (production-ready, no heavy dependencies)

### Backend ✅ Implemented
- **FastAPI** (Python 3.10+) for high-performance REST API
- **Hugging Face Transformers** (BART) for NLP summarization
- **Pydantic** for data validation
- **uv** for fast package management
- **Centralized data management** - threads served via API

## Project Structure

```
ce-email-summarizer/
├── frontend/                   # React TypeScript application
│   ├── public/
│   │   └── threads.json       # Sample email threads data
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ThreadList.tsx
│   │   │   ├── ThreadDetail.tsx
│   │   │   └── SummaryEditor.tsx
│   │   ├── types/
│   │   │   └── thread.ts      # TypeScript interfaces
│   │   ├── App.tsx            # Main application component
│   │   └── main.tsx
│   └── package.json
├── backend/                    # FastAPI application
│   ├── main.py                # FastAPI app with endpoints
│   ├── models.py              # Pydantic data models
│   ├── summarizer.py          # NLP summarization service
│   ├── threads.json           # Email threads data
│   ├── test_api.py            # API test script
│   └── pyproject.toml         # uv dependencies
└── requirements.md            # Detailed requirements document
```

## Features

### ✅ Implemented
**Frontend:**
- **Thread List View**: Browse all customer email threads with status indicators
- **Thread Detail View**: Side-by-side display of original emails and AI summary
- **Summary Editor**: Edit summaries, action items, and metadata
- **Approval Workflow**: Mark summaries as approved for CRM export
- **Responsive Layout**: Split-pane interface optimized for CE associates

**Backend:**
- **FastAPI REST API** with CORS support
- **Threads API** - Centralized data management (GET /api/threads)
- **Real AI Summarization** using Hugging Face BART model (POST /api/summarize)
- **Sentiment Analysis** (rule-based keyword matching)
- **Action Item Extraction** (template-based)
- **Priority Classification** (heuristic analysis)
- **Fallback Summarization** when model unavailable
- **Health Check** with detailed status (GET /health)

### 📋 Planned
- Database persistence
- User authentication
- CRM integration endpoints
- Analytics dashboard
- Batch processing

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+ (for backend)

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**: Navigate to [http://localhost:5173](http://localhost:5173)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or: brew install uv
   ```

3. **Start the API server**:
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The server will:
   - Download the BART model on first run (~1.6GB, takes 3-5 minutes)
   - Fall back to rule-based summarization if download fails
   - Start on http://localhost:8000

4. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Get all threads
   curl http://localhost:8000/api/threads

   # Run test script
   uv run python test_api.py
   ```

5. **View API docs**: http://localhost:8000/docs

## Usage Guide

1. **View Threads**: The left panel shows all available email threads loaded from backend API
2. **Select Thread**: Click on any thread to view details
3. **Generate Summary**: Click "Generate Summary" to create a real AI summary using BART
4. **Review Summary**: Examine the AI-generated summary alongside the original thread
5. **Edit (Optional)**: Click "Edit" to modify the summary or action items
6. **Approve**: Click "Approve Summary" when ready for CRM export

## Data Format

### Input: Email Threads
```json
{
  "thread_id": "CE-405467-683",
  "topic": "Damaged product on arrival",
  "subject": "Order 405467-683: Damaged item received",
  "order_id": "405467-683",
  "product": "LED Monitor",
  "messages": [
    {
      "id": "m1",
      "sender": "customer",
      "timestamp": "2025-09-12T06:39:29",
      "body": "Hello, my item arrived damaged..."
    }
  ]
}
```

### Output: AI Summary
```json
{
  "thread_id": "CE-405467-683",
  "issue_category": "Product Damage",
  "summary": "Customer reported LED Monitor arrived damaged...",
  "sentiment": "frustrated",
  "status": "pending",
  "action_items": [
    "Request customer photos of damage",
    "Process replacement order"
  ],
  "priority": "high"
}
```

## Design Decisions

### Why React + TypeScript?
- **Type Safety**: Prevents runtime errors in production
- **Component Reusability**: Modular architecture for scalability
- **Developer Experience**: Fast iteration with hot module replacement

### Why Vite?
- **Speed**: 10x faster than Create React App
- **Modern**: ES modules, tree-shaking out of the box
- **Lightweight**: Minimal configuration needed

### Why Vanilla CSS?
- **Performance**: No runtime overhead
- **Simplicity**: Easy to understand and modify
- **Production-Ready**: No build-time concerns with CSS-in-JS libraries

### Why FastAPI + Hugging Face?
- **No API Keys Required**: Self-hosted Transformers model
- **Cost Effective**: Zero per-request costs
- **Fast**: Async support for high throughput
- **Type Safe**: Pydantic validation prevents errors

---

## License

MIT License - Feel free to use and modify for your own projects.
