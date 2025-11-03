import { ThreadWithSummary, ThreadSummary } from '../types/thread';
import SummaryEditor from './SummaryEditor';
import './ThreadDetail.css';

interface ThreadDetailProps {
  thread: ThreadWithSummary;
  onSummaryUpdate: (threadId: string, summary: ThreadSummary) => void;
  onSummaryApprove: (threadId: string) => void;
  onGenerateSummary: (threadId: string) => void;
}

const ThreadDetail = ({
  thread,
  onSummaryUpdate,
  onSummaryApprove,
  onGenerateSummary
}: ThreadDetailProps) => {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="thread-detail">
      <div className="thread-detail-header">
        <div className="thread-info">
          <h2>{thread.subject}</h2>
          <div className="thread-meta">
            <span className="order-id">Order: {thread.order_id}</span>
            <span className="separator">•</span>
            <span className="product">{thread.product}</span>
            <span className="separator">•</span>
            <span className="topic">{thread.topic}</span>
          </div>
        </div>

        {!thread.summary && (
          <button
            className="btn btn-primary"
            onClick={() => onGenerateSummary(thread.thread_id)}
          >
            Generate Summary
          </button>
        )}
      </div>

      <div className="thread-detail-content">
        <div className="thread-messages">
          <h3>Email Thread</h3>
          <div className="messages-container">
            {thread.messages.map((message) => (
              <div
                key={message.id}
                className={`message message-${message.sender}`}
              >
                <div className="message-header">
                  <span className="sender">
                    {message.sender === 'customer' ? 'Customer' : 'Company'}
                  </span>
                  <span className="timestamp">{formatTimestamp(message.timestamp)}</span>
                </div>
                <div className="message-body">{message.body}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="thread-summary">
          {thread.summary ? (
            <SummaryEditor
              summary={thread.summary}
              onUpdate={(updatedSummary) => onSummaryUpdate(thread.thread_id, updatedSummary)}
              onApprove={() => onSummaryApprove(thread.thread_id)}
            />
          ) : (
            <div className="summary-placeholder">
              <div className="placeholder-content">
                <svg
                  width="64"
                  height="64"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3>No Summary Generated</h3>
                <p>Click "Generate Summary" to analyze this thread with AI</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ThreadDetail;
