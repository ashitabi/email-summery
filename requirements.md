# CE Email Summarization Prototype - Requirements

## Project Overview
Build a working prototype that summarizes multi-threaded customer experience (CE) email conversations with a human-in-the-loop approval workflow for customer support associates.

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **UI Library**: Material-UI (MUI) or Tailwind CSS
- **State Management**: React Context API or Zustand
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **NLP**: OpenAI GPT-4 API or Anthropic Claude API
- **Data Validation**: Pydantic
- **CORS**: FastAPI CORS middleware
- **Environment**: python-dotenv

### Development Tools
- **Package Manager**: npm/yarn (frontend), pip (backend)
- **Code Quality**: ESLint, Prettier (frontend), Black, Flake8 (backend)
- **Version Control**: Git

## Functional Requirements

### 1. Email Thread Processing
- **Input**: JSON file containing customer email threads
- **Data Structure**:
  - Thread ID, topic, subject, order ID, product
  - Messages with sender, timestamp, body
- **Processing**: Handle noisy data (random numbers, irrelevant words)

### 2. NLP Summarization
- **Core Functionality**:
  - Extract key issues from multi-message threads
  - Identify customer sentiment (frustrated, confused, satisfied)
  - Detect resolution status
  - Extract actionable items
- **Output Structure**:
  ```json
  {
    "thread_id": "string",
    "order_id": "string",
    "product": "string",
    "issue_category": "string",
    "summary": "string",
    "sentiment": "string",
    "status": "string",
    "action_items": ["string"],
    "priority": "low|medium|high"
  }
  ```

### 3. Workflow - Review & Approval
- **View Thread**: Display original email thread with timestamps
- **View Summary**: Show AI-generated summary alongside original
- **Edit**: Allow CE associates to modify the summary
- **Approve/Reject**:
  - Approve: Mark as finalized
  - Reject: Request re-summarization with feedback
- **Export**: Generate output for CRM integration

### 4. User Interface Requirements
- **Dashboard**: List of all email threads with status indicators
- **Thread Detail View**:
  - Left panel: Original email thread
  - Right panel: AI summary with edit capabilities
- **Comparison Mode**: Highlight key points extracted from original
- **Search & Filter**: By order ID, product, status, priority
- **Responsive Design**: Works on desktop (primary) and tablet

## Non-Functional Requirements

### Performance
- **Summarization**: < 5 seconds per thread
- **UI Response**: < 200ms for user interactions
- **Concurrent Users**: Support 10+ CE associates

### Scalability Considerations
- **API Rate Limiting**: Handle LLM API quotas
- **Batch Processing**: Process multiple threads
- **Caching**: Store summaries to avoid re-processing
- **Database Ready**: Design for future database integration

### Security
- **API Keys**: Environment variable management
- **Input Validation**: Sanitize user inputs
- **CORS**: Restrict frontend origins

### Usability
- **Learning Curve**: < 5 minutes for CE associates
- **Error Handling**: Clear error messages
- **Loading States**: Visual feedback during processing

## Data Requirements

### Input Dataset
- **File**: `ce_exercise_threads UPDATED.txt` (JSON format)
- **Threads**: 5 email conversations
- **Topics**:
  1. Damaged product on arrival
  2. Late delivery inquiry
  3. Wrong color/size variant
  4. Return/refund request
  5. Outbound: address confirmation confusion

### Data Processing Challenges
- Messages contain 1-50 words
- High noise ratio (random numbers, unrelated words)
- Context requires understanding across multiple messages
- Initiated by customer or company

## API Endpoints (Backend)

### Thread Management
- `POST /api/threads/upload` - Upload email threads JSON
- `GET /api/threads` - List all threads with summaries
- `GET /api/threads/{thread_id}` - Get specific thread details

### Summarization
- `POST /api/summarize/{thread_id}` - Generate summary for a thread
- `POST /api/summarize/batch` - Batch summarize multiple threads

### Review & Approval
- `PUT /api/threads/{thread_id}/summary` - Update summary
- `POST /api/threads/{thread_id}/approve` - Approve summary
- `POST /api/threads/{thread_id}/reject` - Reject summary with feedback

### Export
- `GET /api/threads/{thread_id}/export` - Export approved summary (CRM format)

## Success Metrics

### Technical Metrics
- Summary accuracy: > 90% key issue identification
- Summary faithfulness: No hallucinations
- Processing time: < 5 seconds per thread
- System uptime: > 99%

### Business Impact
- **Time Saved**: Reduce review time from 5 min to 1 min per thread
- **CSAT**: Improve response accuracy and consistency
- **EBITDA**:
  - 80% time reduction × 100 threads/day × 5 minutes = 400 minutes saved/day
  - ~33 hours/week = 0.8 FTE saved

## Project Scope (3-5 hours)

### In Scope
- Basic working prototype
- Core summarization functionality
- Edit/approve workflow
- Simple UI for demonstration
- Documentation of approach and scaling plan

### Out of Scope (Future Enhancements)
- User authentication/authorization
- Database persistence (use in-memory for now)
- Advanced analytics and reporting
- Real-time email integration
- Multi-language support
- Mobile app

## Development Phases

### Phase 1: Setup (30 min)
- Initialize React TypeScript project
- Initialize FastAPI project
- Set up project structure
- Install dependencies

### Phase 2: Backend Core (90 min)
- Create data models
- Implement LLM integration
- Build summarization logic
- Create API endpoints
- Test with sample data

### Phase 3: Frontend Core (90 min)
- Build thread list view
- Create thread detail component
- Implement summary editor
- Add approve/reject workflow
- Connect to backend APIs

### Phase 4: Integration & Polish (60 min)
- End-to-end testing
- Error handling
- Loading states
- Basic styling
- Documentation

## Deliverables

1. **GitHub Repository** with:
   - Source code (frontend + backend)
   - README with setup instructions
   - Sample data file

2. **Documentation** (< 1 page):
   - Tech stack rationale
   - NLP approach and prompt engineering
   - Scaling plan for production
   - Business impact estimation

3. **Demo-Ready Prototype**:
   - Can be run locally
   - Processes provided dataset
   - Shows complete workflow

## Notes
- Focus on demonstrating the flow rather than perfection
- Document areas for improvement
- Emphasize practical judgment in technology choices
- Show understanding of production considerations
