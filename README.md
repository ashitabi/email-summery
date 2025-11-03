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

### Mock Data Strategy
- **Rapid Prototyping**: Demonstrates full workflow without backend dependency
- **Realistic**: Uses actual noisy data from provided dataset
- **Easy Integration**: Drop-in replacement with API calls when backend is ready

## Scaling Plan

### Phase 1: MVP (Current)
- Frontend wireframe with mock data
- Basic workflow demonstration

### Phase 2: Backend Integration
- FastAPI REST API
- LLM integration (GPT-4/Claude)
- Real-time summarization

### Phase 3: Production Ready
- Database (PostgreSQL)
- Caching layer (Redis)
- Rate limiting and queue management
- Error handling and retry logic

### Phase 4: Advanced Features
- Batch processing pipeline
- Custom fine-tuned models
- Multi-language support
- Analytics and insights

### Infrastructure Considerations
- **Horizontal Scaling**: Stateless API design allows multiple instances
- **Database**: Read replicas for thread retrieval, write leader for updates
- **Caching**: Redis for frequently accessed summaries (60% reduction in DB queries)
- **Queue**: Celery/RabbitMQ for async summarization of large batches
- **Monitoring**: Prometheus + Grafana for performance metrics

## Business Impact

### Time Savings
- **Before**: 5 minutes per thread review (manual reading + summarization)
- **After**: 1 minute per thread review (AI summary + quick verification)
- **Improvement**: 80% time reduction

### ROI Calculation
```
Assumptions:
- 100 threads/day
- 5 minutes → 1 minute per thread
- 4 minutes saved per thread

Daily Savings: 100 threads × 4 min = 400 minutes = 6.7 hours
Weekly Savings: 6.7 hours × 5 days = 33.5 hours
Annual Savings: 33.5 hours × 52 weeks = 1,742 hours ≈ 0.84 FTE

Cost Savings (at $50k/year salary): ~$42,000/year
```

### Additional Benefits
- **CSAT Improvement**: Faster response times and consistent quality
- **Reduced Errors**: AI catches key details humans might miss
- **Scalability**: Handle peak volumes without additional headcount

## Development Timeline

- ✅ **Hour 1**: Requirements analysis and project setup
- ✅ **Hour 2**: Frontend component architecture and wireframes
- ✅ **Hour 3**: Styling and UX polish
- 🔄 **Hour 4**: Backend API and LLM integration (next)
- 📋 **Hour 5**: Testing, documentation, and demo prep

## Known Limitations

1. **Mock Data**: Current version uses predefined summaries, not real AI
2. **No Persistence**: Data resets on page reload
3. **No Backend**: All logic runs in the browser
4. **Single User**: No collaboration features

## Future Enhancements

- [ ] Connect to real LLM API (GPT-4/Claude)
- [ ] Add prompt engineering interface
- [ ] Implement feedback loop for model improvement
- [ ] A/B testing framework for prompt variations
- [ ] Sentiment analysis visualization
- [ ] Export summaries in multiple formats (JSON, CSV, PDF)

## Contributing

This is a prototype for demonstration purposes. For production deployment:
1. Add environment variable management (.env)
2. Implement authentication/authorization
3. Add comprehensive error handling
4. Write unit and integration tests
5. Set up CI/CD pipeline

## License

Proprietary - Created for SDM Customer Experience Assessment

## Contact

For questions or feedback about this prototype, please reach out to the development team.

---

**Note**: This is a working prototype demonstrating the core workflow. The mock summarization will be replaced with real AI integration in the next phase.
