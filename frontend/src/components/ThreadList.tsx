import { ThreadWithSummary } from '../types/thread';
import './ThreadList.css';

interface ThreadListProps {
  threads: ThreadWithSummary[];
  selectedThreadId?: string;
  onThreadSelect: (thread: ThreadWithSummary) => void;
}

const ThreadList = ({ threads, selectedThreadId, onThreadSelect }: ThreadListProps) => {
  const getPriorityBadge = (priority?: string) => {
    if (!priority) return null;
    return <span className={`priority-badge priority-${priority}`}>{priority}</span>;
  };

  const getStatusBadge = (summary?: ThreadWithSummary['summary']) => {
    if (!summary) return <span className="status-badge status-none">No Summary</span>;
    if (summary.isApproved) return <span className="status-badge status-approved">Approved</span>;
    if (summary.isEdited) return <span className="status-badge status-edited">Edited</span>;
    return <span className="status-badge status-pending">Pending</span>;
  };

  return (
    <div className="thread-list">
      <div className="thread-list-header">
        <h2>Email Threads</h2>
        <span className="thread-count">{threads.length} threads</span>
      </div>

      <div className="thread-list-items">
        {threads.map((thread) => (
          <div
            key={thread.thread_id}
            className={`thread-item ${selectedThreadId === thread.thread_id ? 'selected' : ''}`}
            onClick={() => onThreadSelect(thread)}
          >
            <div className="thread-item-header">
              <span className="thread-id">{thread.thread_id}</span>
              {getStatusBadge(thread.summary)}
            </div>

            <div className="thread-item-subject">{thread.subject}</div>

            <div className="thread-item-meta">
              <span className="product">{thread.product}</span>
              <span className="separator">•</span>
              <span className="message-count">{thread.messages.length} messages</span>
            </div>

            {thread.summary && (
              <div className="thread-item-footer">
                <span className="category">{thread.summary.issue_category}</span>
                {getPriorityBadge(thread.summary.priority)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThreadList;
