import { useState } from 'react';
import { ThreadSummary } from '../types/thread';
import './SummaryEditor.css';

interface SummaryEditorProps {
  summary: ThreadSummary;
  onUpdate: (summary: ThreadSummary) => void;
  onApprove: () => void;
}

const SummaryEditor = ({ summary, onUpdate, onApprove }: SummaryEditorProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedSummary, setEditedSummary] = useState(summary.summary);
  const [editedActionItems, setEditedActionItems] = useState(summary.action_items);

  const handleSave = () => {
    onUpdate({
      ...summary,
      summary: editedSummary,
      action_items: editedActionItems
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedSummary(summary.summary);
    setEditedActionItems(summary.action_items);
    setIsEditing(false);
  };

  const handleActionItemChange = (index: number, value: string) => {
    const newActionItems = [...editedActionItems];
    newActionItems[index] = value;
    setEditedActionItems(newActionItems);
  };

  const handleAddActionItem = () => {
    setEditedActionItems([...editedActionItems, '']);
  };

  const handleRemoveActionItem = (index: number) => {
    setEditedActionItems(editedActionItems.filter((_, i) => i !== index));
  };

  const getSentimentColor = (sentiment: string) => {
    const colors: Record<string, string> = {
      positive: '#10b981',
      neutral: '#6b7280',
      negative: '#ef4444',
      frustrated: '#f59e0b'
    };
    return colors[sentiment] || colors.neutral;
  };

  return (
    <div className="summary-editor">
      <div className="summary-header">
        <h3>AI Summary</h3>
        <div className="summary-badges">
          {summary.isApproved && <span className="badge badge-approved">Approved</span>}
          {summary.isEdited && !summary.isApproved && <span className="badge badge-edited">Edited</span>}
        </div>
      </div>

      <div className="summary-metadata">
        <div className="metadata-item">
          <label>Category</label>
          <span className="value">{summary.issue_category}</span>
        </div>
        <div className="metadata-item">
          <label>Sentiment</label>
          <span
            className="value sentiment"
            style={{ color: getSentimentColor(summary.sentiment) }}
          >
            {summary.sentiment}
          </span>
        </div>
        <div className="metadata-item">
          <label>Status</label>
          <span className="value">{summary.status}</span>
        </div>
        <div className="metadata-item">
          <label>Priority</label>
          <span className={`value priority-${summary.priority}`}>
            {summary.priority}
          </span>
        </div>
      </div>

      <div className="summary-content">
        <div className="summary-section">
          <div className="section-header">
            <h4>Summary</h4>
            {!isEditing && !summary.isApproved && (
              <button className="btn btn-secondary btn-sm" onClick={() => setIsEditing(true)}>
                Edit
              </button>
            )}
          </div>
          {isEditing ? (
            <textarea
              className="summary-textarea"
              value={editedSummary}
              onChange={(e) => setEditedSummary(e.target.value)}
              rows={6}
            />
          ) : (
            <p className="summary-text">{summary.summary}</p>
          )}
        </div>

        <div className="summary-section">
          <div className="section-header">
            <h4>Action Items</h4>
            {isEditing && (
              <button className="btn btn-secondary btn-sm" onClick={handleAddActionItem}>
                + Add
              </button>
            )}
          </div>
          <ul className="action-items">
            {isEditing ? (
              editedActionItems.map((item, index) => (
                <li key={index} className="action-item-edit">
                  <input
                    type="text"
                    value={item}
                    onChange={(e) => handleActionItemChange(index, e.target.value)}
                    className="action-item-input"
                  />
                  <button
                    className="btn-icon btn-remove"
                    onClick={() => handleRemoveActionItem(index)}
                    aria-label="Remove"
                  >
                    ×
                  </button>
                </li>
              ))
            ) : (
              summary.action_items.map((item, index) => (
                <li key={index} className="action-item">
                  <span className="checkbox">□</span>
                  {item}
                </li>
              ))
            )}
          </ul>
        </div>
      </div>

      <div className="summary-actions">
        {isEditing ? (
          <>
            <button className="btn btn-secondary" onClick={handleCancel}>
              Cancel
            </button>
            <button className="btn btn-primary" onClick={handleSave}>
              Save Changes
            </button>
          </>
        ) : (
          <>
            {summary.isApproved ? (
              <div className="approved-message">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
                </svg>
                <span>Summary approved and ready for CRM export</span>
              </div>
            ) : (
              <button className="btn btn-success" onClick={onApprove}>
                Approve Summary
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default SummaryEditor;
